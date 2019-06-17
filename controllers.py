# Imports, sorted alphabetically.

# Python packages
import socket
import time
import datetime
from functools import partial
import subprocess

from math import cos, sin, pi, fmod
import operator
import os
import sys
import random


# Third-party packages
import threading
from pyglet.gl import *
from pyglet import image

# Modules from this project
from blocks import *
from cameras import Camera3D
from client import PacketReceiver
import globals as G
from gui import ItemSelector, InventorySelector, TextWidget
from items import Tool
from player import Player
from model import PlayerModel
from skydome import Skydome
import utils
from utils import vec, sectorize, normalize, load_image, image_sprite
import views
from world import World
from biome import BiomeGenerator
from server import start_server

__all__ = (
    'Controller', 'MainMenuController', 'GameController',
)


class Controller:
    def __init__(self, window):
        self.window = window
        self.current_view = None
        utils.init_resources()

    def setup(self):
        pass

    def update(self, dt):
        if self.current_view:
            self.current_view.update(dt)

    def switch_view(self, new_view):
        if self.current_view:
            self.current_view.pop_handlers()
            self.current_view = None
        self.current_view = new_view
        self.current_view.add_handlers()
        return pyglet.event.EVENT_HANDLED

    def switch_view_class(self, new_view_class):
        self.switch_view(new_view_class(self))
        return pyglet.event.EVENT_HANDLED

    def switch_controller(self, controller):
        self.window.switch_controller(controller)
        return pyglet.event.EVENT_HANDLED

    def switch_controller_class(self, controller_class):
        self.switch_controller(controller_class(self.window))
        return pyglet.event.EVENT_HANDLED


    def set_2d(self):
        width, height = self.window.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def push_handlers(self):
        self.window.push_handlers(self)
        self.setup()

    def pop_handlers(self):
        if self.current_view:
            self.current_view.pop_handlers()
        self.window.pop_handlers()

class MainMenuController(Controller):

    def __init__(self, *args, **kwargs):
        super(MainMenuController, self).__init__(*args, **kwargs)
        self.setup = partial(self.switch_view_class, views.MainMenuView)
        self.game_options = partial(self.switch_view_class, views.OptionsView)
        self.main_menu = partial(self.switch_view_class, views.MainMenuView)
        self.controls = partial(self.switch_view_class, views.ControlsView)
        self.textures = partial(self.switch_view_class, views.TexturesView)
        self.multiplayer = partial(self.switch_view_class, views.MultiplayerView)
        self.sound = partial(self.switch_view_class, views.SoundView)
        self.feedback = lambda: self.switch_view_class(views.FeedbackView)
        self.exit_game = pyglet.app.exit

    def start_singleplayer_game(self):
        G.SINGLEPLAYER = True
        self.switch_controller_class(GameController)

    def start_multiplayer_game(self):
        G.SINGLEPLAYER = False
        self.switch_controller_class(GameController)

class GameController(Controller):
    def __init__(self, window):
        super(GameController, self).__init__(window)
        self.sector, self.highlighted_block, self.crack, self.last_key = (None,) * 4
        self.bg_red, self.bg_green, self.bg_blue = (0.0,) * 3
        self.mouse_pressed, self.sorted = (False,) * 2
        self.count, self.block_damage = (0,) * 2
        self.light_y, self.light_z = (1.0,) * 2
        self.time_of_day = 0.0
        self.hour_deg = 15.0
        self.clock = 6

        self.back_to_main_menu = threading.Event()

    def update(self, dt):
        if self.back_to_main_menu.isSet():
            self.switch_controller_class(MainMenuController)
            return
        self.update_sector(dt)
        self.update_player(dt)
        self.update_mouse(dt)
        self.update_time()
        self.camera.update(dt)

    def update_sector(self, dt):
        sector = sectorize(self.player.position)
        if sector != self.sector:
            self.world.change_sectors(sector)
            # When the world is loaded, show every visible sector.
            if self.sector is None:
                self.world.process_entire_queue()
            self.sector = sector

    def update_player(self, dt):
        m = 8
        df = min(dt, 0.2)
        for _ in range(m):
            self.player.update(df / m, self)
        for ply in self.player_ids.values():
            for _ in range(m):
                ply.update(df / m, self)
        momentum = self.player.get_motion_vector(15 if self.player.flying else 5*self.player.current_density)
        if momentum != self.player.momentum_previous:
            self.player.momentum_previous = momentum
            self.packetreceiver.send_movement(momentum, self.player.position)


    def update_mouse(self, dt):
        if self.mouse_pressed:
            vector = self.player.get_sight_vector()
            block, previous = self.world.hit_test(self.player.position, vector,
                                                  self.player.attack_range)
            self.set_highlighted_block(block)

            if self.highlighted_block:
                hit_block = self.world[self.highlighted_block]
                if hit_block.hardness >= 0:
                    self.update_block_damage(dt, hit_block)
                    self.update_block_remove(dt, hit_block)

    def update_block_damage(self, dt, hit_block):
        multiplier = 1
        current_item = self.item_list.get_current_block()
        if current_item is not None:
            if isinstance(current_item, Tool):  # tool
                if current_item.tool_type == hit_block.digging_tool:
                    multiplier = current_item.multiplier

        self.block_damage += self.player.attack_power * dt * multiplier

    def update_block_remove(self, dt, hit_block):
        if self.block_damage >= hit_block.hardness:
            self.world.remove_block(self.player,
                                    self.highlighted_block)
            self.set_highlighted_block(None)
            if getattr(self.item_list.get_current_block_item(), 'durability', -1) != -1:
                self.item_list.get_current_block_item().durability -= 1
                if self.item_list.get_current_block_item().durability <= 0:
                    self.item_list.remove_current_block()
                    self.item_list.update_items()
            if hit_block.drop_id is None:
                return
            if type(hit_block.drop_id) == list:
                for index, item in enumerate(hit_block.drop_id):
                    if not self.player.add_item(item, quantity=hit_block.drop_quantity[index]):
                        return
            elif not self.player.add_item(hit_block.drop_id, quantity=hit_block.drop_quantity):
                    return
            self.item_list.update_items()
            self.inventory_list.update_items()

    def init_gl(self):
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0.1)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_BLEND)

        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_POLYGON_SMOOTH)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)

        # glClampColorARB(GL_CLAMP_VERTEX_COLOR_ARB, GL_FALSE)
        # glClampColorARB(GL_CLAMP_FRAGMENT_COLOR_ARB, GL_FALSE)
        # glClampColorARB(GL_CLAMP_READ_COLOR_ARB, GL_FALSE)

        # glClearColor(0, 0, 0, 0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def setup(self):
        if G.SINGLEPLAYER:
            try:
                print('Starting internal server...')
                # TODO: create world menu
                G.SAVE_FILENAME = "world"
                start_server()
                time.sleep(3)
                sock = socket.socket()
                sock.connect((socket.gethostbyname(socket.gethostname()), 1486))
            except socket.error as e:
                print("Socket Error:", e)
                # Otherwise back to the main menu we go
                return False
            except Exception as e:
                print('Unable to start internal server')
                import traceback
                traceback.print_exc()
                return False
        else:
            try:
                # Make sure the address they want to connect to works
                ipport = G.IP_ADDRESS.split(":")
                if len(ipport) == 1: ipport.append(1486)
                sock = socket.socket()
                sock.connect((tuple(ipport)))
            except socket.error as e:
                print("Socket Error:", e)
                # Otherwise back to the main menu we go
                return False

        self.init_gl()

        sky_rotation = -20.0  # -20.0

       # TERRAIN_CHOICE = self.biome_generator.get_biome_type(sector[0], sector[2])
        default_skybox = 'skydome.jpg'
        #if TERRAIN_CHOICE == G.NETHER:
        #    default_skybox = 'skydome_nether.jpg'
        #else:
        #    default_skybox = 'skybox.jpg'


        self.skydome = Skydome(
            G.RESOURCES + default_skybox,
            #'resources/skydome.jpg',
            0.7,
            100.0,
            sky_rotation,
        )

        self.player_ids = {}  # Dict of all players this session, indexes are their ID's [0: first Player on server,]

        self.focus_block = Block(width=1.05, height=1.05)
        self.earth = vec(0.8, 0.8, 0.8, 1.0)
        self.white = vec(1.0, 1.0, 1.0, 1.0)
        self.ambient = vec(1.0, 1.0, 1.0, 1.0)
        self.polished = GLfloat(100.0)
        self.crack_batch = pyglet.graphics.Batch()

        #if G.DISABLE_SAVE and world_exists(G.game_dir, G.SAVE_FILENAME):
        #    open_world(self, G.game_dir, G.SAVE_FILENAME)

        self.world = World()
        self.packetreceiver = PacketReceiver(self.world, self, sock)
        self.world.packetreceiver = self.packetreceiver
        G.CLIENT = self.packetreceiver
        self.packetreceiver.start()

        #Get our position from the server
        self.packetreceiver.request_spawnpos()
        #Since we don't know it yet, lets disable self.update, or we'll load the wrong chunks and fall
        self.update_disabled = self.update
        self.update = lambda dt: None
        #We'll re-enable it when the server tells us where we should be

        self.player = Player(game_mode=G.GAME_MODE)
        print(('Game mode: ' + self.player.game_mode))
        self.item_list = ItemSelector(self, self.player, self.world)
        self.inventory_list = InventorySelector(self, self.player, self.world)
        self.item_list.on_resize(self.window.width, self.window.height)
        self.inventory_list.on_resize(self.window.width, self.window.height)
        self.text_input = TextWidget(self.window, '',
                                     0, 0,
                                     self.window.width,
                                     visible=False,
                                     font_name=G.CHAT_FONT)
        self.text_input.push_handlers(on_toggled=self.on_text_input_toggled, key_released=self.text_input_callback)
        self.chat_box = TextWidget(self.window, '',
                                   0, self.text_input.y + self.text_input.height + 50,
                                   self.window.width // 2, height=min(300, self.window.height // 3),
                                   visible=False, multi_line=True, readonly=True,
                                   font_name=G.CHAT_FONT,
                                   text_color=(255, 255, 255, 255),
                                   background_color=(0, 0, 0, 100),
                                   enable_escape=True)
        self.camera = Camera3D(target=self.player)

        if G.HUD_ENABLED:
            self.label = pyglet.text.Label(
                '', font_name='Arial', font_size=8, x=10, y=self.window.height - 10,
                anchor_x='left', anchor_y='top', color=(255, 255, 255, 255))

        #if G.DEBUG_TEXT_ENABLED:
        #    self.debug_text = TextWidget(self.window, '',
        #                           0, self.window.height - 300,
        #                           500, 300,
        #                           visible=True, multi_line=True, readonly=True,
        #                           font_name='Arial', font_size=10,
        #                           text_color=(255, 255, 255, 255),
        #                           background_color=(0, 0, 0, 0))
        pyglet.clock.schedule_interval_soft(self.world.process_queue,
                                            1.0 / G.MAX_FPS)
        pyglet.clock.schedule_interval_soft(self.world.hide_sectors, 10.0, self.player)
        return True

    def update_time(self):
        """
        The idle function advances the time of day.
        The day has 24 hours, from sunrise to sunset and from sunrise to
        second sunset.
        The time of day is converted to degrees and then to radians.
        """

        if not self.window.exclusive:
            return

        time_of_day = self.time_of_day if self.time_of_day < 12.0 \
            else 24.0 - self.time_of_day

        if time_of_day <= 2.5:
            self.time_of_day += 1.0 / G.TIME_RATE
            time_of_day += 1.0 / G.TIME_RATE
            self.count += 1
        else:
            self.time_of_day += 20.0 / G.TIME_RATE
            time_of_day += 20.0 / G.TIME_RATE
            self.count += 1.0 / 20.0
        if self.time_of_day > 24.0:
            self.time_of_day = 0.0
            time_of_day = 0.0

        side = len(self.world.sectors) * 2.0

        self.light_y = 2.0 * side * sin(time_of_day * self.hour_deg
                                        * G.DEG_RAD)
        self.light_z = 2.0 * side * cos(time_of_day * self.hour_deg
                                        * G.DEG_RAD)
        if time_of_day <= 2.5:
            ambient_value = 1.0
        else:
            ambient_value = 1 - (time_of_day - 2.25) / 9.5
        self.ambient = vec(ambient_value, ambient_value, ambient_value, 1.0)

        # Calculate sky colour according to time of day.
        sin_t = sin(pi * time_of_day / 12.0)
        self.bg_red = 0.1 * (1.0 - sin_t)
        self.bg_green = 0.9 * sin_t
        self.bg_blue = min(sin_t + 0.4, 0.8)

        if fmod(self.count / 2, G.TIME_RATE) == 0:
            if self.clock == 18:
                self.clock = 6
            else:
                self.clock += 1

        self.skydome.update_time_of_day(self.time_of_day)

    def set_highlighted_block(self, block):
        if self.highlighted_block == block:
            return
        self.highlighted_block = block
        self.block_damage = 0
        if self.crack:
            self.crack.delete()
        self.crack = None

    def on_mouse_press(self, x, y, button, modifiers):
        if self.window.exclusive:
            vector = self.player.get_sight_vector()
            block, previous = self.world.hit_test(self.player.position, vector, self.player.attack_range)
            if button == pyglet.window.mouse.LEFT:
                self.on_mouse_press_left(block, x, y, button, modifiers)
            else:
                self.on_mouse_press_right(block, previous, x, y, button, modifiers)
        else:
            self.window.set_exclusive_mouse(True)

    def on_mouse_press_left(self, block, x, y, button, modifiers):
        if block:
            self.mouse_pressed = True
            self.set_highlighted_block(None)

    def on_mouse_press_right(self, block, previous, x, y, button, modifiers):
        if previous:
            hit_block = self.world[block]
            if hit_block.id == craft_block.id:
                self.inventory_list.switch_mode(1)
                self.inventory_list.toggle(False)
            elif hit_block.id == furnace_block.id:
                self.inventory_list.switch_mode(2)
                self.inventory_list.set_furnace(hit_block)
                self.inventory_list.toggle(False)
            elif hit_block.density >= 1:
               self.put_block(previous)
        elif self.item_list.get_current_block() and getattr(self.item_list.get_current_block(), 'regenerated_health', 0) != 0 and self.player.health < self.player.max_health:
            self.eat_item()

    def put_block(self, previous): # FIXME - Better name...
        current_block = self.item_list.get_current_block()
        if current_block is not None:
            if current_block.id.is_item():
                if current_block.on_right_click(self.world, self.player):
                    self.item_list.get_current_block_item().change_amount(-1)
                    self.item_list.update_health()
                    self.item_list.update_items()
            else:
                localx, localy, localz = map(operator.sub,previous,normalize(self.player.position))
                if localx != 0 or localz != 0 or (localy != 0 and localy != -1):
                    self.world.add_block(previous, current_block)
                    self.item_list.remove_current_block()

    def eat_item(self): # FIXME - Better name (2)...
        self.player.change_health(self.item_list.get_current_block().regenerated_health)
        self.item_list.get_current_block_item().change_amount(-1)
        self.item_list.update_health()
        self.item_list.update_items()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.window.exclusive:
            self.set_highlighted_block(None)
            self.mouse_pressed = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.window.exclusive:
            m = 0.15
            x, y = self.player.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.player.rotation = (x, y)
            self.camera.rotate(x, y)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.on_mouse_motion(x, y, dx, dy)

    def on_key_press(self, symbol, modifiers):
        if symbol == G.TOGGLE_HUD_KEY:
            G.HUD_ENABLED = not G.HUD_ENABLED
        if symbol == G.TOGGLE_DEBUG_TEXT_KEY:
            #self.debug_text.visible = not self.debug_text.visible
            G.DEBUG_TEXT_ENABLED = not G.DEBUG_TEXT_ENABLED
        elif symbol == G.INVENTORY_SORT_KEY:
            if self.last_key == symbol and not self.sorted:
                self.player.quick_slots.sort()
                self.player.inventory.sort()
                self.sorted = True
            else:
                self.player.quick_slots.change_sort_mode()
                self.player.inventory.change_sort_mode()
                self.item_list.update_items()
                self.inventory_list.update_items()
        elif symbol == G.INVENTORY_KEY:
            self.set_highlighted_block(None)
            self.mouse_pressed = False
            self.inventory_list.toggle()
        elif symbol == G.SOUND_UP_KEY:
            G.EFFECT_VOLUME = min(G.EFFECT_VOLUME + .1, 1)
        elif symbol == G.SOUND_DOWN_KEY:
            G.EFFECT_VOLUME = max(G.EFFECT_VOLUME - .1, 0)
        elif symbol == G.SCREENCAP_KEY:  # dedicated screencap key
            now = datetime.datetime.now()
            dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
            st = dt.strftime('%Y-%m-%d_%H.%M.%S')
            filename = str(st) + '.png'
            if not os.path.exists('screencaptures'):
                os.makedirs('screencaptures')
            path = 'screencaptures/' + filename
            pyglet.image.get_buffer_manager().get_color_buffer().save(path)
        elif symbol == G.SHOWMAP_KEY:
            self.show_map()
        self.last_key = symbol

    def on_key_release(self, symbol, modifiers):
        if symbol == G.TALK_KEY:
            self.toggle_text_input()
            return pyglet.event.EVENT_HANDLED

    def on_resize(self, width, height):
        if G.HUD_ENABLED:
            self.label.y = height - 10
        self.text_input.resize(x=0, y=0, width=self.window.width)
        self.chat_box.resize(x=0, y=self.text_input.y + self.text_input.height + 50,
                             width=self.window.width // 2, height=min(300, self.window.height // 3))
        #self.debug_text.resize(0, self.window.height - 300,
        #                           500, 300)

    def set_3d(self):
        width, height = self.window.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(G.FOV, width / float(height),
                       G.NEAR_CLIP_DISTANCE,
                       G.FAR_CLIP_DISTANCE)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        self.camera.look()
        self.skydome.draw()
        glPopMatrix()
        self.camera.transform()

    def clear(self):
        glClearColor(self.bg_red, self.bg_green, self.bg_blue, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def on_draw(self):
        self.clear()
        #self.window.clear()
        self.set_3d()
        #glColor3d(1, 1, 1)
        self.world.batch.draw()
        self.world.transparency_batch.draw()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.crack_batch.draw()
        glDisable(GL_BLEND)
        self.draw_focused_block()
        for ply in self.player_ids.values():
            ply.model.draw()
        self.set_2d()
        if G.HUD_ENABLED:
            self.draw_label()
            self.item_list.draw()
            self.inventory_list.draw()
        #if G.DEBUG_TEXT_ENABLED:
        #    self.update_label()
        #self.debug_text.draw()
        self.text_input.draw()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.chat_box.draw()
        glDisable(GL_BLEND)

    def show_cracks(self, hit_block, vertex_data):
        if self.block_damage:  # also show the cracks
            crack_level = int(CRACK_LEVELS * self.block_damage
                              // hit_block.hardness)  # range: [0, CRACK_LEVELS[
            if crack_level >= CRACK_LEVELS:
                return
            texture_data = crack_textures.texture_data[crack_level]
            count = len(texture_data) // 2
            if self.crack:
                self.crack.delete()
            self.crack = self.crack_batch.add(count, GL_QUADS, crack_textures.group,
                                              ('v3f/static', vertex_data),
                                              ('t2f/static', texture_data))

    def draw_focused_block(self):
        glDisable(GL_LIGHTING)
        vector = self.player.get_sight_vector()
        position = self.world.hit_test(self.player.position, vector, self.player.attack_range)[0]
        if position:
            hit_block = self.world[position]
            if hit_block.density >= 1:
                self.focus_block.width = hit_block.width * 1.05
                self.focus_block.height = hit_block.height * 1.05
                vertex_data = self.focus_block.get_vertices(*position)

                if hit_block.hardness > 0.0:
                    self.show_cracks(hit_block, vertex_data)

                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glColor4f(0.0, 0.0, 0.0, 0.4)
                glLineWidth(2.0)
                glDisable(GL_TEXTURE_2D)
                glDepthMask(False)

                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

                glDepthMask(True)
                glEnable(GL_TEXTURE_2D)
                glDisable(GL_BLEND)

    def draw_label(self):
        x, y, z = self.player.position
        self.label.text = 'Time:%.1f Inaccurate FPS:%02d (%.2f, %.2f, %.2f) Blocks Shown: %d / %d sector_packets:%d'\
                          % (self.time_of_day if (self.time_of_day < 12.0)
               else (24.0 - self.time_of_day),
               pyglet.clock.get_fps(), x, y, z,
               len(self.world._shown), len(self.world), len(self.world.sector_packets))
        self.label.draw()

    def update_label(self):
        x, y, z = self.player.position
        self.debug_text.clear()
        self.debug_text.write_line(' '.join((G.APP_NAME, str(G.APP_VERSION))))
        self.debug_text.write_line('Time:%.1f Inaccurate FPS:%02d Blocks Shown: %d / %d sector_packets:%d'\
                          % (self.time_of_day if (self.time_of_day < 12.0)
               else (24.0 - self.time_of_day),
               pyglet.clock.get_fps(),
               len(self.world._shown), len(self.world), len(self.world.sector_packets)))
        self.debug_text.write_line('x: %.2f, sector: %d' %(x, x // G.SECTOR_SIZE))
        self.debug_text.write_line('y: %.2f, sector: %d' %(y, y // G.SECTOR_SIZE))
        self.debug_text.write_line('z: %.2f, sector: %d' %(z, z // G.SECTOR_SIZE))
        #dirs = ['East', 'South', 'West', 'North']
        #vec, direction, angle = self.player.get_sight_direction()
        #dx, dy, dz = vec
        #self.debug_text.write_line('Direction: (%.2f, %.2f, %.2f) %d(%s) %.2f' % (dx, dy, dz, direction, dirs[direction], angle))

    def write_line(self, text, **kwargs):
        self.chat_box.write_line(text, **kwargs)

    def text_input_callback(self, symbol, modifier):
        if symbol == G.VALIDATE_KEY:
            txt = self.text_input.text.replace('\n', '')
            self.text_input.clear()
            if txt:
                self.world.packetreceiver.send_chat(txt)
            return pyglet.event.EVENT_HANDLED

    def hide_chat_box(self, dt):
        self.chat_box.toggle(False)

    def on_text_input_toggled(self):
        pyglet.clock.unschedule(self.hide_chat_box)  # Disable the fade timer
        self.chat_box.toggle(state=self.text_input.visible)  # Pass through the state incase chat_box was already visible
        if self.chat_box.visible:
            self.chat_box.focused = True # Allow scrolling
            self.window.push_handlers(self.chat_box)
        else:
            self.chat_box.focused = False
            self.window.remove_handlers(self.chat_box)

    def toggle_text_input(self):
        self.text_input.toggle()
        if self.text_input.visible:
            self.player.velocity = 0
            self.player.strafe = [0, 0]
            self.window.push_handlers(self.text_input)
            self.text_input.focus()
        else:
            self.window.remove_handlers(self.text_input)

    def push_handlers(self):
        if self.setup():
            self.window.push_handlers(self.camera)
            self.window.push_handlers(self.player)
            self.window.push_handlers(self)
            self.window.push_handlers(self.item_list)
            self.window.push_handlers(self.inventory_list)
        else:
            self.switch_controller_class(MainMenuController)

    def pop_handlers(self):
        while self.window._event_stack:
            self.window.pop_handlers()

    def on_close(self):
        G.save_config()
        self.world.packetreceiver.stop()  # Disconnect from the server so the process can close
        if hasattr(self, 'local_server_process'):
            print("Stopping Local Server...")
            self.local_server_process.stdin.write("stop")
            self.local_server_process.stdin.close()
            self.local_server_stdout_thread.join()
            print("Local Server stopped.")

    def show_map(self):
        print("map called...")
         # taken from Nebual's biome_explorer, this is ment to be a full screen map that uses mini tiles to make a full 2d map.
        with open(os.path.join(G.game_dir, "world", "seed"), "r") as f:
            SEED = f.read()
        b = BiomeGenerator(SEED)
        x, y, z = self.player.position
        curx =  x
        cury = y
        xsize = 79
        ysize = 28
        pbatch = pyglet.graphics.Batch()
        pgroup = pyglet.graphics.OrderedGroup(1)
        DESERT, PLAINS, MOUNTAINS, SNOW, FOREST = list(range(5))
        letters = ["D","P","M","S","F"]

        #  temp background pic...
        image = load_image('resources', 'textures', 'main_menu_background.png')

        #map_frame = image_sprite(image, pbatch, 0, y=G.WINDOW_WIDTH, height=G.WINDOW_HEIGHT)
        #sprite = pyglet.sprite.Sprite(image)
        #sprite.image(image)
        #sprite.visible = True
       # map_frame.draw()
       # map_frame.visible = True
        for y in range(int(cury),int(cury+ysize)):
         for x in range(int(curx),int(curx+xsize)):
             #string += letters[b.get_biome_type(x,y)]
            tmap = letters[b.get_biome_type(x,y)]
            tile_map = load_image('resources', 'textures', tmap +'.png')
            tile_map.anchor_x = x * 8
            tile_map.anchor_y = y * 8
            sprite = pyglet.sprite.Sprite(tile_map, x=x * 8, y=y * 8, batch=pbatch)
            game_map = image_sprite(tile_map, pbatch, pgroup, x * 8, y * 8, 8, 8)
            game_map = pyglet.sprite.Sprite(image,x=G.WINDOW_WIDTH, y=G.WINDOW_HEIGHT,batch=pbatch, group=pgroup)
            game_map = pyglet.sprite.Sprite(tile_map,x=x*8, y=y*8,batch=pbatch, group=pgroup)

            tile_map.blit(x *8, y * 8)

            #tile_map.draw()
            #map.append(tmap)
            game_map.draw()
            pbatch.draw()
            ## Save to file, did not work...
        #map.image.save('mapX.png')
        # map_streamX = open('mapX2.png', 'wb')
        # tile_map.save('mapX2.png', file=map_streamX)
        # #tile_map.image_data = map.image
        # map.visible = True
        # map_stream2 = open('map2.png', 'wb')
        # tile_map.save('map2.png', file=map_stream2)
        # map_stream = open('map.png', 'wb')
        # #map.save('map_test.png', file=map_stream)
        # tile_map.save('map.png', file=map_stream)

        #            string += "\n"
        #        print string + "Current position: (%s-%s %s-%s)" % (curx*8, (curx+xsize)*8, cury*8, (cury+ysize)*8)
