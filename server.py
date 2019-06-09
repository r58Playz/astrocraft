#!/usr/bin/env python3

from _socket import SHUT_RDWR
import socket
import struct
import time
import timer
import socketserver
import threading

import globals as G
from custom_types import fVector, iVector
from savingsystem import save_sector_to_bytes, save_blocks, save_world, load_player, save_player
from world_server import WorldServer
import blocks
from text_commands import CommandParser, COMMAND_HANDLED, CommandException, COMMAND_ERROR_COLOR
from utils import sectorize, make_string_packet
from mod import load_modules

#This class is effectively a serverside "Player" object
class ServerPlayer(socketserver.BaseRequestHandler):
    id: int
    position: fVector
    momentum: fVector
    username: str
    inventory = b"\0"*(4*40)  # Currently, is serialized to be 4 bytes * (27 inv + 9 quickbar + 4 armor) = 160 bytes
    command_parser = CommandParser()
    server: 'Server'

    operator = False

    def sendpacket(self, size: int, packet: bytes):
        self.request.sendall(struct.pack("i", 5 + size) + packet)

    def send_sector(self, world: WorldServer, sector: iVector):
        if sector not in world.sectors:
            with world.server_lock:
                world.open_sector(sector)

        if not world.sectors[sector]:
            # Empty sector, send packet 2
            self.sendpacket(12, b"\2" + struct.pack("iii", *sector))
        else:
            packet = struct.pack("iii", *sector) \
                     + save_sector_to_bytes(world, sector) \
                     + world.get_exposed_sector(sector)
            self.sendpacket(len(packet), b"\1" + packet)

    def sendchat(self, txt: str, color=(255,255,255,255)):
        txt_bytes = txt.encode('utf-8')
        self.sendpacket(len(txt_bytes) + 4, b"\5" + txt_bytes + struct.pack("BBBB", *color))
    def sendinfo(self, info: str, color=(255,255,255,255)):
        info_bytes = info.encode('utf-8')
        self.sendpacket(len(info_bytes) + 4, b"\5" + info_bytes + struct.pack("BBBB", *color))
    def broadcast(self, txt: str):
        for player in self.server.players.values():
            player.sendchat(txt)
    def sendpos(self, pos_bytes, mom_bytes):
        self.sendpacket(38, b"\x08" + struct.pack("H", self.id) + mom_bytes + pos_bytes)

    def lookup_player(self, playername):
        # find player by name
        for player in list(self.server.players.values()):
            if player.username == playername:
                return player
        return None

    def handle(self):
        self.username = str(self.client_address)
        print("Client connecting...", self.client_address)
        self.server.players[self.client_address] = self
        self.server.player_ids.append(self)
        self.id = len(self.server.player_ids) - 1
        try:
            self.loop()
        except socket.error as e:
            if self.server._stop.isSet():
                return  # Socket error while shutting down doesn't matter
            if e.errno in (32, 10053, 10054):
                print("Client %s %s crashed." % (self.username, self.client_address))
            else:
                raise e

    def loop(self):
        world, players = self.server.world, self.server.players
        while 1:
            byte = self.request.recv(1)
            if not byte: return  # The client has disconnected intentionally

            packettype = struct.unpack("B", byte)[0]  # Client Packet Type
            if packettype == 1:  # Sector request
                sector = struct.unpack("iii", self.request.recv(4*3))

                if sector not in world.sectors:
                    with world.server_lock:
                        world.open_sector(sector)

                if not world.sectors[sector]:
                    # Empty sector, send packet 2
                    self.sendpacket(12, b"\2" + struct.pack("iii",*sector))
                else:
                    self.send_sector(world, sector)
            elif packettype == 3:  # Add block
                positionbytes = self.request.recv(4*3)
                blockbytes = self.request.recv(2)

                position = struct.unpack("iii", positionbytes)
                blockid = G.BLOCKS_DIR[struct.unpack("BB", blockbytes)]
                with world.server_lock:
                    world.add_block(position, blockid, sync=False)

                for address in players:
                    if address is self.client_address: continue  # He told us, we don't need to tell him
                    players[address].sendpacket(14, b"\3" + positionbytes + blockbytes)
            elif packettype == 4:  # Remove block
                positionbytes = self.request.recv(4*3)

                with world.server_lock:
                    world.remove_block(struct.unpack("iii", positionbytes), sync=False)

                for address in players:
                    if address is self.client_address: continue  # He told us, we don't need to tell him
                    players[address].sendpacket(12, b"\4" + positionbytes)
            elif packettype == 5:  # Receive chat text
                txtlen = struct.unpack("i", self.request.recv(4))[0]
                raw_txt = self.request.recv(txtlen).decode('utf-8')
                txt = "%s: %s" % (self.username, raw_txt)
                try:
                    if raw_txt[0] == '/':
                        ex = self.command_parser.execute(raw_txt, user=self, world=world)
                        if ex != COMMAND_HANDLED:
                            self.sendchat('$$rUnknown command.')
                    else:
                        # Not a command, send the chat to all players
                        for address in players:
                            players[address].sendchat(txt)
                        print(txt)  # May as well let console see it too
                except CommandException as e:
                    self.sendchat(str(e), COMMAND_ERROR_COLOR)
            elif packettype == 6:  # Player Inventory Update
                self.inventory = self.request.recv(4*40)
                #TODO: All player's inventories should be autosaved at a regular interval.
            elif packettype == 8:  # Player Movement
                mom_bytes, pos_bytes = self.request.recv(4*3), self.request.recv(8*3)
                self.momentum = struct.unpack("fff", mom_bytes)
                self.position = struct.unpack("ddd", pos_bytes)
                for address in players:
                    if address is self.client_address: continue  # He told us, we don't need to tell him
                    #TODO: Only send to nearby players
                    players[address].sendpacket(38, b"\x08" + struct.pack("H", self.id) + mom_bytes + pos_bytes)
            elif packettype == 9:  # Player Jump
                for address in players:
                    if address is self.client_address: continue  # He told us, we don't need to tell him
                    #TODO: Only send to nearby players
                    players[address].sendpacket(2, b"\x09" + struct.pack("H", self.id))
            elif packettype == 10: # Update Tile Entity
                block_pos = struct.unpack("iii", self.request.recv(4*3))
                ent_size = struct.unpack("i", self.request.recv(4))[0]
                world[block_pos].update_tile_entity(self.request.recv(ent_size))
            elif packettype == 255:  # Initial Login
                txtlen = struct.unpack("i", self.request.recv(4))[0]
                self.username = self.request.recv(txtlen).decode('utf-8')
                load_player(self, "world")

                for player in self.server.players.values():
                    player.sendchat("$$y%s has connected." % self.username)
                print("%s's username is %s" % (self.client_address, self.username))

                position = (0,self.server.world.terraingen.get_height(0,0)+2,0)
                if self.position is None:
                    # New player, set initial position
                    self.position = (0.0, world.terraingen.get_height(0, 0) + 2.0, 0.0)
                elif self.position[1] < 0:
                    # Somehow fell below the world, reset their height
                    self.position = (self.position[0], world.terraingen.get_height(0, 0) + 2.0, self.position[2])

                # Send list of current players to the newcomer
                for player in self.server.players.values():
                    if player is self: continue
                    name = player.username.encode('utf-8')
                    self.sendpacket(2 + len(name), b'\7' + struct.pack("H", player.id) + name)
                # Send the newcomer's name to all current players
                name = self.username.encode('utf-8')
                for player in self.server.players.values():
                    if player is self: continue
                    player.sendpacket(2 + len(name), b'\7' + struct.pack("H", self.id) + name)

                # Send them the sector under their feet first so they don't fall
                sector = sectorize(self.position)
                self.send_sector(world, sector)
                if sector[1] > 0:
                    sector_below = (sector[0], sector[1] - 1, sector[2])
                    self.send_sector(world, sector_below)

                #Send them their spawn position and world seed(for client side biome generator)
                if not G.SEED:
                    try:
                        seed = int(hexlify(os.urandom(16)), 16)
                    except (NotImplementedError, NameError):
                        seed = int(time.time() * 256)
                    G.SEED = seed
                seed_packet = make_string_packet(str(G.SEED))
                self.sendpacket(12 + len(seed_packet),
                                struct.pack("B", 255) + struct.pack("fff", *self.position) + seed_packet)
                self.sendpacket(4*40, b"\6" + self.inventory)
            else:
                print("Received unknown packettype", packettype)
    def finish(self):
        print("Client disconnected,", self.client_address, self.username)
        try: del self.server.players[self.client_address]
        except KeyError: pass
        for player in self.server.players.values():
            player.sendchat("%s has disconnected." % self.username)
        # Send user list
        for player in self.server.players.values():
            player.sendpacket(2 + 1, b'\7' + struct.pack("H", self.id) + b'\0')
        save_player(self, "world")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, *args, **kwargs):
        socketserver.ThreadingTCPServer.__init__(self, *args, **kwargs)
        self._stop = threading.Event()

        self.world = WorldServer(self)
        self.players = {}  # Dict of all players connected. {ipaddress: requesthandler,}
        self.player_ids = []  # List of all players this session, indexes are their ID's [0: first requesthandler,]

        self.command_parser = CommandParser()

    def show_block(self, position, block):
        blockid = block.id
        for player in self.players.values():
            #TODO: Only if they're in range
            player.sendpacket(14, b"\3" + struct.pack("iiiBB", *(position+(blockid.main, blockid.sub))))

    def hide_block(self, position):
        for player in self.players.values():
            #TODO: Only if they're in range
            player.sendpacket(12, b"\4" + struct.pack("iii", *position))

    def update_tile_entity(self, position, value: bytes):
        for player in self.players.values():
            player.sendpacket(12 + len(value), b"\x0A" + struct.pack("iii", *position) + value)


def start_server(internal=False):
    if internal:
        localip = "localhost"
    else:
        localip = socket.gethostbyname(socket.gethostname())
    server = Server((localip, 1486), ServerPlayer)
    G.SERVER = server
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    threading.Thread(target=server.world.content_update, name="world_server.content_update").start()

    # start server timer
    G.main_timer = timer.Timer(G.TIMER_INTERVAL, name="G.main_timer")
    G.main_timer.start()

    return server, server_thread


if __name__ == '__main__':
    #TODO: Enable server launch options
    #In the mean time, manually set
    setattr(G.LAUNCH_OPTIONS, "seed", None)
    G.SAVE_FILENAME = "world"

    load_modules(server=True)

    server, server_thread = start_server()
    print(('Server loop running in thread: ' + server_thread.name))

    ip, port = server.server_address
    print("Listening on",ip,port)

    helptext = "Available commands: " + ", ".join(["say", "stop", "save"])
    while 1:
        args = input().strip().split(" ")
        cmd = args.pop(0)
        if cmd == "say":
            msg = "Server: %s" % " ".join(args)
            print(msg)
            for player in server.players.values():
                player.sendchat(msg, color=(180,180,180,255))
        elif cmd == "help":
            print(helptext)
        elif cmd == "save":
            print("Saving...")
            save_world(server, "world")
            print("Done saving")
        elif cmd == "stop":
            server._stop.set()
            G.main_timer.stop()
            print("Disconnecting clients...")
            for address in server.players.keys():
                try:
                    server.players[address].request.shutdown(SHUT_RDWR)
                    server.players[address].request.close()
                except socket.error:
                    pass
            print("Shutting down socket...")
            server.shutdown()
            print("Saving...")
            save_world(server, "world")
            print("Goodbye")
            break
        else:
            print("Unknown command '%s'." % cmd, helptext)
    while len(threading.enumerate()) > 1:
        threads = threading.enumerate()
        for t in threads:
            if hasattr(t, 'do_kill_pydev_thread'):
                t.do_kill_pydev_thread()
        threads.remove(threading.current_thread())
        print("Waiting on these threads to close:", threads)
        time.sleep(1)
