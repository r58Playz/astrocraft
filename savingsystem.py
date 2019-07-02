# Imports, sorted alphabetically.

# Python packages
import os
import struct
from typing import Optional

# Third-party packages
import msgpack

# Modules from this project
import custom_types
from blocks import BlockID
from custom_types import iVector
import globals as G


__all__ = (
    'sector_to_filename', 'region_to_filename', 'sector_to_region',
    'sector_to_offset', 'save_world', 'world_exists', 'remove_world',
    'sector_exists', 'load_region',
)


structvec = struct.Struct("hhh")
structushort = struct.Struct("H")
structuchar2 = struct.Struct("BB")
structvecBB = struct.Struct("hhhBB")

null2 = struct.pack("xx") #Two \0's
null1024 = null2*512      #1024 \0's
air = BlockID(0)


def sector_to_filename(secpos: iVector) -> str:
    x,y,z = secpos
    return "%i.%i.%i.pyr" % (x//4, y//4, z//4)


def region_to_filename(region: iVector) -> str:
    return "%i.%i.%i.pyr" % region


def sector_to_region(secpos: iVector) -> iVector:
    x,y,z = secpos
    return (x//4, y//4, z//4)


def sector_to_offset(secpos: iVector) -> int:
    x,y,z = secpos
    return ((x % 4)*16 + (y % 4)*4 + (z % 4)) * 1024


def sector_to_blockpos(secpos: iVector) -> iVector:
    x,y,z = secpos
    return x*8, y*8, z*8


def save_sector_to_bytes(blocks: custom_types.WorldServer, secpos: iVector) -> bytes:
    cx, cy, cz = sector_to_blockpos(secpos)
    fstr = b""
    for x in range(cx, cx+8):
        for y in range(cy, cy+8):
            for z in range(cz, cz+8):
                blk = blocks.get((x, y, z), air) if isinstance(blocks.get((x, y, z), air), BlockID) else blocks.get((x, y, z), air).id
                if blk is not air.main:
                    # if isinstance(blk, int): # When does this occur? Its expensive and I don't see it triggering
                    #     blk = BlockID(blk)
                    fstr += structuchar2.pack(blk.main, blk.sub)
                else:
                    fstr += null2
    return fstr


def save_world(server: custom_types.Server, world: str):
    # Non block related data
    # save = (4,window.player, window.time_of_day, G.SEED)
    # pickle.dump(save, open(os.path.join(game_dir, world, "save.pkl"), "wb"))
    import multiprocessing

    def sve():
        save_blocks(server.world, world)

    pool = multiprocessing.Pool()
    pool.map(sve, tuple())
    pool.close()
    for player in server.players:
        save_player(player, world)

def save_quit_world(server, world: str = "world"):
    import multiprocessing

    def sve():
        import threading
        threading.Thread(target=lambda: save_blocks(server.world, world))
        for player in server.players:
            save_player(player, world)

    pool = multiprocessing.Pool()
    pool.map(sve, tuple())
    pool.close()


def autosave(server, world: str = "world"):
    import threading
    threading.Thread(target=lambda: save_blocks(server.world, world))
    for player in server.players:
        threading.Thread(target=lambda: save_player(player, world))
    return True


def save_blocks(blocks: custom_types.WorldServer, world: str):
    # blocks and sectors (window.world and window.world.sectors)
    # Saves individual sectors in region files (4x4x4 sectors)

    for secpos in blocks.sectors:  # TODO: only save dirty sectors
        if not blocks.sectors[secpos]:
            continue  # Skip writing empty sectors
        file = os.path.join(G.game_dir, world, sector_to_filename(secpos))
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.truncate(64*1024)  # Preallocate the file to be 64kb
        with open(file, "rb+") as f:  # Load up the region file
            f.seek(sector_to_offset(secpos))  # Seek to the sector offset
            f.write(save_sector_to_bytes(blocks, secpos))


def save_player(player: custom_types.ServerPlayer, world: str):
    # We have to implement our own serialization layer since msgpack cannot pack custom classes.
    plyer = (player.position, player.momentum if getattr(player, "momentum") else (0,0,0), player.inventory)
    bytes_player = msgpack.packb(plyer, use_bin_type=True)
    with open(os.path.join(G.game_dir, world, player.username), 'wb') as fo:
        fo.write(bytes_player)

    # sqlite3(bigger file size)
    # db = connect_db(world)
    # cur = db.cursor()
    # cur.execute('insert or replace into players(version, pos_x, pos_y, pos_z, mom_x, mom_y, mom_z, inventory, name) ' + \
    #     "values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (1,
    #         player.position[0], player.position[1], player.position[2],
    #         player.momentum[0], player.momentum[1], player.momentum[2],
    #         player.inventory, player.username))
    # db.commit()
    # cur.close()
    # db.close()


def world_exists(world=None):
    if world is None: world = "world"
    return os.path.lexists(os.path.join(G.worlds_dir, world))


def remove_world(world=None):
    if world is None: world = "world"
    if world_exists(world):
        import shutil
        shutil.rmtree(os.path.join(G.worlds_dir, world))


def sector_exists(sector, world=None):
    if world is None:
        world = "world"
    return os.path.lexists(os.path.join(G.game_dir, world, sector_to_filename(sector)))


def load_region(world: custom_types.WorldServer, world_name: str = "world", region: Optional[iVector] = None,
                sector: Optional[iVector] = None):
    sectors = world.sectors
    blocks = world
    SECTOR_SIZE = G.SECTOR_SIZE
    BLOCKS_DIR = G.BLOCKS_DIR
    if sector: region = sector_to_region(sector)
    rx, ry, rz = region
    rx, ry, rz = rx*32, ry*32, rz*32
    with open(os.path.join(G.game_dir, world_name, region_to_filename(region)), "rb") as f:
        # Load every chunk in this region (4x4x4)
        for cx in range(rx, rx+32, 8):
            for cy in range(ry, ry+32, 8):
                for cz in range(rz, rz+32, 8):
                    # Now load every block in this chunk (8x8x8)
                    fstr = f.read(1024)
                    if fstr != null1024:
                        fpos = 0
                        for x in range(cx, cx+8):
                            for y in range(cy, cy+8):
                                for z in range(cz, cz+8):
                                    read = fstr[fpos:fpos+2]
                                    fpos += 2
                                    if read != null2:
                                        position = x, y, z
                                        try: 
                                            full_id = structuchar2.unpack(read)
                                            blocks[position] = BLOCKS_DIR[full_id]
                                            if blocks[position].sub_id_as_metadata:
                                                blocks[position] = type(BLOCKS_DIR[full_id])()
                                                blocks[position].set_metadata(full_id[-1])
                                        except KeyError:
                                            try:
                                                main_blk = BLOCKS_DIR[(full_id[0], 0)]
                                                if main_blk.sub_id_as_metadata: # sub id is metadata
                                                    blocks[position] = type(main_blk)()
                                                    blocks[position].set_metadata(full_id[-1])
                                            except KeyError:
                                                sectors[(x//SECTOR_SIZE, y//SECTOR_SIZE, z//SECTOR_SIZE)].append(position)


def load_player(player, world: str):
    if os.path.exists(os.path.join(G.game_dir, world, player.username)):
        fo = open(os.path.join(G.game_dir, world, player.username),'rb')
    else:
        player.position = None
        player.momentum = (0, 0, 0)
        player.inventory = (struct.pack("HBB", 0, 0, 0)) * 40
        return
    # We have to implement our own serialization layer since msgpack cannot unpack custom classes.
    lst = msgpack.unpackb(fo.read(), raw=False)
    player.position = lst[0]
    player.momentum = lst[1]
    player.inventory = lst[2]
    fo.close()

    # sqlite3(bigger file size)
    # db = connect_db(world)
    # cur = db.cursor()
    # cur.execute("select * from players where name='%s'" % player.username)
    # data = cur.fetchone()
    # if data is None:    # no such entry, set initial value
    #     player.position = None
    #     player.momentum = (0, 0, 0)
    #     player.inventory = (struct.pack("HBB", 0, 0, 0)) * 40
    # else:
    #     player.position = list(data[i] for i in range(2, 5))
    #     player.momentum = list(data[i] for i in range(5, 8))
    #     player.inventory = data[8]
    # cur.close()
    # db.close()
