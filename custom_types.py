from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    # this is always False at runtime, but this lets us work around cyclic import dependencies
    from blocks import Block, BlockID
    from items import Item, ItemStack

    from player import Player
    from world import World

    from server import Server, ServerPlayer
    from world_server import WorldServer
else:
    Block = None
    BlockID = None
    Item = None
    ItemStack = None

    Player = None
    World = None

    Server = None
    ServerPlayer = None
    WorldServer = None

iVector = Tuple[int, int, int]
fVector = Tuple[float, float, float]
