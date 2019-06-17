# Imports, sorted alphabetically.

# Python packages
import os
import struct
from typing import Tuple, List, Union
from ctypes import byref
from subprocess import Popen
import sys
import threading

# Third-party packages
import pyglet
from pyglet.gl import *

# Modules from this project
import globals as G
from custom_types import iVector, fVector


__all__ = (
    'load_image', 'image_sprite', 'hidden_image_sprite', 'vec', 'FastRandom',
    'init_resources', 'init_font', 'get_block_icon',
    'logstream', 'FACES', 'FACES_WITH_DIAGONALS', 'normalize_float', 'normalize',
    'sectorize', 'TextureGroup', 'make_nbt_from_dict', 'extract_nbt'
)


def load_image(*args):
    path = os.path.join(*args)
    return pyglet.image.load(os.path.join(*args)) if os.path.isfile(
        path) else None


def image_sprite(image, batch, group, x: int = 0, y: int = 0, width: int = None, height: int = None):
    if image is None or batch is None or group is None:
        return None
    width = width or image.width
    height = height or image.height
    if isinstance(group, int):
        group = pyglet.graphics.OrderedGroup(group)
    return pyglet.sprite.Sprite(image.get_region(x, y, width, height),
                                batch=batch, group=group)


def hidden_image_sprite(*args, **kwargs):
    sprite = image_sprite(*args, **kwargs)
    if sprite:
        sprite.visible = False
    return sprite


def vec(*args):
    """Creates GLfloat arrays of floats"""
    return (GLfloat * len(args))(*args)


# fast math algorithms
class FastRandom:
    seed: int
    def __init__(self, seed):
        self.seed = seed

    def randint(self) -> int:
        self.seed = (214013 * int(self.seed) + 2531011)
        return (self.seed >> 16) & 0x7FFF


def logstream(io_stream, logger_callback):
    """A threading helper, which runs the callback (ie. print) for each line in the io_stream"""
    while True:
        out = io_stream.readline()
        if out:
            logger_callback(out.rstrip())
        else:
            break




def init_resources():
    init_font(G.RESOURCES + 'fonts\\Chunkfive.ttf', 'ChunkFive Roman')
    init_font(G.RESOURCES + 'fonts\\slkscr.ttf', 'Silkscreen Normal')


def init_font(filename, fontname):
    pyglet.font.add_file(filename)
    pyglet.font.load(fontname)



_block_icon_fbo = None

def get_block_icon(block, icon_size, world):
    global _block_icon_fbo

    block_icon = G.texture_pack_list.selected_texture_pack.load_texture(block.id.filename()) \
        or (block.group or world.group).texture.get_region(
            int(block.texture_data[2 * 8] * G.TILESET_SIZE) * icon_size,
            int(block.texture_data[2 * 8 + 1] * G.TILESET_SIZE) * icon_size,
            icon_size,
            icon_size)

    if block.id.is_item():
        return block_icon

    # create 3d icon for blocks
    if _block_icon_fbo is None:
        _block_icon_fbo = GLuint(0)
        glGenFramebuffers(1, byref(_block_icon_fbo))

    glBindFramebuffer(GL_FRAMEBUFFER, _block_icon_fbo)

    icon_texture = pyglet.image.Texture.create(icon_size, icon_size, GL_RGBA)
    glBindTexture(GL_TEXTURE_2D, icon_texture.id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, icon_size, icon_size, 0, GL_RGBA, GL_FLOAT, None)

    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, icon_texture.id, 0)

    viewport = (GLint * 4)()
    glGetIntegerv(GL_VIEWPORT, viewport)
    glViewport(0, 0, icon_size, icon_size)

    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -10, 10)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glRotatef(-45.0, 0.0, 1.0, 0.0)
    glRotatef(-30.0, -1.0, 0.0, 1.0)
    glScalef(1.5, 1.5, 1.5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    vertex_data = block.get_vertices(0, 0, 0)
    texture_data = block.texture_data
    count = len(texture_data) // 2
    batch = pyglet.graphics.Batch()
    batch.add(count, GL_QUADS, (block.group or world.group),
              ('v3f/static', vertex_data),
              ('t2f/static', texture_data))
    batch.draw()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glBindFramebuffer(GL_FRAMEBUFFER, 0)

    glViewport(*viewport)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    return icon_texture.get_image_data()


FACES: Tuple[iVector, ...] = (
    ( 0,  1,  0),
    ( 0, -1,  0),
    (-1,  0,  0),
    ( 1,  0,  0),
    ( 0,  0,  1),
    ( 0,  0, -1),
)

FACES_WITH_DIAGONALS: Tuple[iVector, ...] = FACES + (
    (-1, -1,  0),
    (-1,  0, -1),
    ( 0, -1, -1),
    ( 1,  1,  0),
    ( 1,  0,  1),
    ( 0,  1,  1),
    ( 1, -1,  0),
    ( 1,  0, -1),
    ( 0,  1, -1),
    (-1,  1,  0),
    (-1,  0,  1),
    ( 0, -1,  1),
)


def normalize_float(f: float) -> int:
    """
    This is faster than int(round(f)).  Nearly two times faster.
    Since it is run at least 500,000 times during map generation,
    and also in game logic, it has a major impact on performance.

    >>> normalize_float(0.2)
    0
    >>> normalize_float(-0.4)
    0
    >>> normalize_float(0.5)
    1
    >>> normalize_float(-0.5)
    -1
    >>> normalize_float(0.0)
    0
    """
    int_f = int(f)
    if f > 0:
        if f - int_f < 0.5:
            return int_f
        return int_f + 1
    if f - int_f > -0.5:
        return int_f
    return int_f - 1


def normalize(position: fVector) -> fVector:
    x, y, z = position
    return normalize_float(x), normalize_float(y), normalize_float(z)


def sectorize(position: Union[iVector, fVector]) -> iVector:
    return (normalize_float(float(position[0])) // G.SECTOR_SIZE,
            normalize_float(float(position[1])) // G.SECTOR_SIZE,
            normalize_float(float(position[2])) // G.SECTOR_SIZE)

cmd = None

def runserver():
    global cmd
    def run():
        global cmd
        with Popen([sys.executable, 'server.py']) as process:
            while True:
                if cmd == "stop":
                    process.stdin.write('stop')
                    process.stdin.flush()
                    return
                elif 'say' in cmd:
                    process.stdin.write(cmd)
                    process.stdin.flush()
                else:
                    continue
    threading.Thread(target=run).start()



class TextureGroup(pyglet.graphics.Group):
    def __init__(self, path):
        super(TextureGroup, self).__init__()
        self.texture = pyglet.image.load(path).get_texture()

    def set_state(self):
        glBindTexture(self.texture.target, self.texture.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glEnable(self.texture.target)

    def unset_state(self):
        glDisable(self.texture.target)

# Named Binary Tag
def make_int_packet(i: int) -> bytes:
    return struct.pack('i', i)

def extract_int_packet(packet: bytes):
    """
    :rtype: (bytes, int)
    """
    return packet[4:], struct.unpack('i', packet[:4])[0]

def make_string_packet(s: str) -> bytes:
    return struct.pack('i', len(s)) + s.encode('utf-8')

def extract_string_packet(packet: bytes):
    """
    :rtype: (bytes, str)
    """
    strlen = struct.unpack('i', packet[:4])[0]
    packet = packet[4:]
    s = packet[:strlen].decode('utf-8')
    packet = packet[strlen:]
    return packet, s

def make_packet(obj) -> bytes:
    if type(obj) == int:
        return make_int_packet(obj)
    elif type(obj) == str:
        return make_string_packet(obj)
    else:
        print(('make_packet: unsupported type: ' + str(type(obj))))
        return None

def extract_packet(packet):
    tag, packet = struct.unpack('B', packet[:1])[0], packet[1:]
    if tag == 0:
        return extract_int_packet(packet)
    elif tag == 1:
        return extract_string_packet(packet)

def type_tag(t) -> bytes:
    tag = 0
    if t == int:
        tag = 0
    elif t == str:
        tag = 1
    return struct.pack('B', tag)

def make_nbt_from_dict(d: dict) -> bytes:
    packet = b''
    for key in list(d.keys()):
        packet += make_string_packet(key) + type_tag(type(d[key])) + make_packet(d[key])
    return packet

def extract_nbt(nbt):
    result = {}
    while len(nbt) > 0:
        nbt, key = extract_string_packet(nbt)
        nbt, value = extract_packet(nbt)
        result[key] = value

    return result

def send_feedback(feedbackstr):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.connect('smtp.gmail.com', 587)
    s.starttls()
    s.login("mhfeedbk@gmail.com", "MHfeedb1k")  # This account is completely new, if you want to use another account,
                                                 # use a new one to prevent leakages of passwords.

    msg = MIMEMultipart()
    message = "Feedback from %s \n\n\n" % (G.USERNAME,) + feedbackstr
    msg['From'] = "mhfeedbk@gmail.com"
    msg['To'] = "toshit307@gmail.com"
    msg['Subject'] = "Feedback from " + G.USERNAME + "!"
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
