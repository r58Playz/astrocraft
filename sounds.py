# Imports, sorted alphabetically.

# Python packages
import time
import threading
import random

# Third-party packages
import pyglet.media

# Modules from this project
import globals as G
import custom_types


__all__ = (
    'wood', 'wood1', 'wood2', 'wood3', 'splash', 'leaves', 'glass', 'dirt',
    'gravel', 'stone', 'melon_break', 'sand', 'play_sound',
)

pyglet.options['audio'] = ('openal', 'directsound', 'pulse', 'silent')

# Note: Pyglet uses /'s regardless of OS
pyglet.resource.path = [".", "resources/sounds"]
pyglet.resource.reindex()

wood = pyglet.resource.media("wood.wav", streaming=False)
wood1 = pyglet.resource.media("wood1.wav", streaming=False)
wood2 = pyglet.resource.media("wood2.wav", streaming=False)
wood3 = pyglet.resource.media("wood3.wav", streaming=False)
wood4 = pyglet.resource.media("wood4.wav", streaming=False)
wood5 = pyglet.resource.media("wood5.wav", streaming=False)
wood6 = pyglet.resource.media("wood6.wav", streaming=False)
splash = pyglet.resource.media("splash.wav", streaming=False)
splash1 = pyglet.resource.media("splash1.wav", streaming=False)
leaves = pyglet.resource.media("leaves.wav", streaming=False)
glass = pyglet.resource.media("glass.wav", streaming=False)
glass1 = pyglet.resource.media("glass1.wav", streaming=False)
glass2 = pyglet.resource.media("glass2.wav", streaming=False)
dirt = pyglet.resource.media("dirt.wav", streaming=False)
gravel = pyglet.resource.media("gravel.wav", streaming=False)
gravel1 = pyglet.resource.media("gravel1.wav", streaming=False)
gravel2 = pyglet.resource.media("gravel2.wav", streaming=False)
gravel3 = pyglet.resource.media("gravel3.wav", streaming=False)
gravel4 = pyglet.resource.media("gravel4.wav", streaming=False)
stone = pyglet.resource.media("stone.wav", streaming=False)
stone1 = pyglet.resource.media("stone1.wav", streaming=False)
stone2 = pyglet.resource.media("stone2.wav", streaming=False)
stone3 = pyglet.resource.media("stone3.wav", streaming=False)
stone4 = pyglet.resource.media("stone4.wav", streaming=False)
stone5 = pyglet.resource.media("stone5.wav", streaming=False)
stone6 = pyglet.resource.media("stone6.wav", streaming=False)
melon_break = pyglet.resource.media("melon_break.wav", streaming=False)
sand = pyglet.resource.media("sand.wav", streaming=False)
sand1 = pyglet.resource.media("sand1.wav", streaming=False)
sand2 = pyglet.resource.media("sand2.wav", streaming=False)
sand3 = pyglet.resource.media("sand3.wav", streaming=False)
sand4 = pyglet.resource.media("sand4.wav", streaming=False)
sand5 = pyglet.resource.media("sand5.wav", streaming=False)
cloth = pyglet.resource.media("cloth.wav", streaming=False)
cloth1 = pyglet.resource.media("cloth1.wav", streaming=False)
cloth2 = pyglet.resource.media("cloth2.wav", streaming=False)
cloth3 = pyglet.resource.media("cloth3.wav", streaming=False)


def play_sound(sound, player: custom_types.Player, position=None):
    sound_player = pyglet.media.Player()

    try:
        driver = pyglet.media.drivers.silent.SilentAudioDriver
    except:
        # If the silent driver cannot be loaded, then sound is available
        try:
            listener = pyglet.media.get_audio_driver().get_listener()
            listener.volume = G.EFFECT_VOLUME
            listener.forward_orientation = player.get_sight_vector()
            if position:
                listener.position = player.position
                sound_player.position = position
            sound_player.volume = G.EFFECT_VOLUME
            sound_player.queue(sound)
            sound_player.play()
            time.sleep(1)
        except:
            return sound_player, False

    return sound_player


