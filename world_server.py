from binascii import hexlify
from collections import deque, defaultdict, OrderedDict
import os
import threading
import time
import warnings
import datetime
from sqlite3.dbapi2 import Connection
from threading import Lock
from typing import Any, Dict, DefaultDict, Deque, Tuple, Optional, Set

from blocks import *
from custom_types import iVector
import savingsystem
from utils import FACES, FACES_WITH_DIAGONALS, normalize_float, normalize, sectorize, TextureGroup
import globals as G
from nature import TREES, TREE_BLOCKS
import terrain


class WorldServer(dict):
    sectors: DefaultDict[iVector, list]
    exposed_cache: Dict[iVector, bytes]
    spreading_mutable_blocks: Deque[iVector]
    server_lock: Lock
    server: Any
    terraingen: terrain.TerrainGeneratorSimple
    spreading_mutations = {
        dirt_block: grass_block,
    }

    def __init__(self, server):
        super(WorldServer, self).__init__()
        if not os.path.lexists(os.path.join(G.game_dir, "world", "players")):
            os.makedirs(os.path.join(G.game_dir, "world", "players"))

        self.sectors = defaultdict(list)
        self.exposed_cache = dict()

        self.spreading_mutable_blocks = deque()

        self.server_lock = threading.Lock()
        self.server = server

        if os.path.exists(os.path.join(G.game_dir, G.SAVE_FILENAME, "seed")):
            with open(os.path.join(G.game_dir, G.SAVE_FILENAME, "seed"), "rb") as f:
                G.SEED = int(f.read().decode('utf-8'))
        else:
            if not os.path.exists(os.path.join(G.game_dir, G.SAVE_FILENAME)): os.makedirs(os.path.join(G.game_dir, G.SAVE_FILENAME))
            with open(os.path.join(G.game_dir, G.SAVE_FILENAME, "seed"), "wb") as f:
                f.write(str(self.generate_seed()).encode('utf-8'))

        self.terraingen = terrain.TerrainGeneratorSimple(self, G.SEED)

    def __delitem__(self, position):
        try:
            super(WorldServer, self).__delitem__(position)
        except KeyError: pass

        if position in self.spreading_mutable_blocks:
            try:
                self.spreading_mutable_blocks.remove(position)
            except ValueError:
                warnings.warn('Block %s was unexpectedly not found in the '
                              'spreading mutations; your save is probably '
                              'corrupted' % repr(position))

    def add_block(self, position: iVector, block, sync: bool = True, force: bool = True, check_spread: bool = True):
        if position in self:
            if not force:
                return
            self.remove_block(position, sync=sync, check_spread=check_spread)
        if hasattr(block, 'entity_type'):
            self[position] = type(block)()
            self[position].entity = self[position].entity_type(self, position)
        elif block.sub_id_as_metadata:
            self[position] = type(block)()
            self[position].set_metadata(block.get_metadata())
        else:
            self[position] = block
        self.sectors[sectorize(position)].append(position)
        if sync:
            self.server.show_block(position, block)
        if check_spread:
            if self.is_exposed(position):
                self.check_spreading_mutable(position, block)
            self.check_neighbors(position)

    def init_block(self, position: iVector, block):
        self.add_block(position, block, sync=False, force=False, check_spread=False)

    def remove_block(self, position: iVector, sync: bool = True, check_spread: bool = True):
        del self[position]
        sector_position = sectorize(position)
        try:
            self.sectors[sector_position].remove(position)
        except ValueError:
            pass
        if sync:
            self.server.hide_block(position)
        if check_spread:
            self.check_neighbors(position)

    def is_exposed(self, position: iVector) -> bool:
        x, y, z = position
        for fx,fy,fz in FACES:
            other_position = (fx+x, fy+y, fz+z)
            if other_position not in self or self[other_position].transparent:
                return True
        return False

    def get_exposed_sector_cached(self, sector: iVector) -> bytes:
        """
        Cached. Returns a 512 length string of 0's and 1's if blocks are exposed
        """
        if sector not in self.exposed_cache:
            self.exposed_cache[sector] = self.get_exposed_sector(sector)
        return self.exposed_cache[sector]

    def get_exposed_sector(self, sector: iVector) -> bytes:
        """ Returns a 512 length string of 0's and 1's if blocks are exposed """
        cx,cy,cz = savingsystem.sector_to_blockpos(sector)
        # Most ridiculous list comprehension ever, but this is 25% faster than using appends
        return b"".join([(x,y,z) in self and self.is_exposed((x,y,z)) and b"1" or b"0"
                        for x in range(cx, cx+8) for y in range(cy, cy+8) for z in range(cz, cz+8)])

    def neighbors_iterator(self, position: iVector, relative_neighbors_positions: Tuple[iVector, ...] = FACES):
        x, y, z = position
        for dx, dy, dz in relative_neighbors_positions:
            yield x + dx, y + dy, z + dz

    def check_neighbors(self, position: iVector):
        for other_position in self.neighbors_iterator(position):
            if other_position not in self:
                continue
            if self.is_exposed(other_position):
                self.check_spreading_mutable(other_position,
                    self[other_position])

    def check_spreading_mutable(self, position: iVector, block):
        x, y, z = position
        above_position: iVector = (x, y + 1, z)
        if above_position in self\
           or position in self.spreading_mutable_blocks\
        or not self.is_exposed(position):
            return
        if block in self.spreading_mutations and self.has_neighbors(
            position,
            is_in={self.spreading_mutations[block]},
            diagonals=True):
            self.spreading_mutable_blocks.appendleft(position)

    def has_neighbors(self, position: iVector,
                      is_in: Optional[Set[iVector]] = None,
                      diagonals: bool = False,
                      faces: Optional[Tuple[iVector, ...]] = None) -> bool:
        if faces is None:
            faces = FACES_WITH_DIAGONALS if diagonals else FACES
        for other_position in self.neighbors_iterator(
            position, relative_neighbors_positions=faces):
            if other_position in self:
                if is_in is None or self[other_position] in is_in:
                    return True
        return False

    def generate_seed(self):
        seed = G.LAUNCH_OPTIONS.seed
        if seed is None:
            # Generates pseudo-random number.
            try:
                seed = int(hexlify(os.urandom(16)), 16)
            except NotImplementedError:
                seed = int(time.time() * 256)  # use fractional seconds

            print(('No seed set, generated random seed: ' + str(seed)))
        G.SEED = seed

        with open(os.path.join(G.game_dir, 'seeds.txt'), 'a') as seeds:
            seeds.write(datetime.datetime.now().strftime('Seed used the %d %m %Y at %H:%M:%S\n'))
            seeds.write('%s\n\n' % seed)
        return seed

    def open_sector(self, sector: iVector):
        # The sector is not in memory, load or create it
        if savingsystem.sector_exists(sector):
            # If its on disk, load it
            savingsystem.load_region(self, sector=sector)
        else:
            # The sector doesn't exist yet, generate it!
            bx, by, bz = savingsystem.sector_to_blockpos(sector)
            rx, ry, rz = bx//32*32, by//32*32, bz//32*32

            # For ease of saving/loading, queue up generation of a whole region (4x4x4 sectors) at once
            yiter, ziter = range(ry//8,ry//8+4), range(rz//8,rz//8+4)
            for secx in range(rx//8,rx//8+4):
                for secy in yiter:
                    for secz in ziter:
                        self.terraingen.generate_sector((secx,secy,secz))

    # run in its own thread
    def autosave(self):
        import time
        while True:
            if G.SERVER._stop.isSet():
                break
            time.sleep(10)
            print("Autosaving...")
            savingsystem.autosave(G.SERVER)

    # content_update is run in its own thread
    def content_update(self):
        # Updates spreading
        # TODO: This is too simple
        while 1:
            time.sleep(G.SPREADING_MUTATION_DELAY)
            if self.server._stop.isSet():
                break  # Close the thread
            if self.spreading_mutable_blocks:
                with self.server_lock:
                    try:
                        position = self.spreading_mutable_blocks.pop()
                        self.add_block(position,
                                       self.spreading_mutations[self[position]], check_spread=False)
                    except KeyError:
                        return

    def generate_vegetation(self, position: iVector, vegetation_class):
        if position in self:
            return

        # Avoids a tree from touching another.
        if vegetation_class in TREES and self.has_neighbors(position, is_in=TREE_BLOCKS, diagonals=True):
            return

        x, y, z = position

        # Vegetation can't grow on anything.
        if self[(x, y - 1, z)] not in vegetation_class.grows_on:
            return

        vegetation_class.add_to_world(self, position)
