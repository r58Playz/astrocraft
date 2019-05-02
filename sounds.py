# Imports, sorted alphabetically.

# Python packages
# Nothing for now...

# Third-party packages
import pyglet.media

# Modules from this project
import globals as G
import custom_types


__all__ = (
    'wood_break', 'water_break', 'leaves_break', 'glass_break', 'dirt_break',
    'gravel_break', 'stone_break', 'melon_break', 'sand_break', 'play_sound',
    'loop_1', 'loop_2', 'loop_3', 'loop_4', 'loop_options', 'play_looping_sound',
)

pyglet.options['audio'] = ('openal', 'directsound', 'pulse', 'silent')

# Note: Pyglet uses /'s regardless of OS
pyglet.resource.path = [".", "resources/sounds"]
pyglet.resource.reindex()

wood_break = pyglet.resource.media("wood_break.wav", streaming=False)
water_break = pyglet.resource.media("water_break.wav", streaming=False)
leaves_break = pyglet.resource.media("leaves_break.wav", streaming=False)
glass_break = pyglet.resource.media("glass_break.wav", streaming=False)
dirt_break = pyglet.resource.media("dirt_break.wav", streaming=False)
gravel_break = pyglet.resource.media("gravel_break.wav", streaming=False)
stone_break = pyglet.resource.media("stone_break.wav", streaming=False)
melon_break = pyglet.resource.media("melon_break.wav", streaming=False)
sand_break = pyglet.resource.media("sand_break.wav", streaming=False)
loop_1 = pyglet.resource.media("background/1.wav", streaming=False)
loop_2 = pyglet.resource.media("background/2.wav", streaming=False)
loop_3 = pyglet.resource.media("background/3.wav", streaming=False)
loop_4 = pyglet.resource.media("background/4.wav", streaming=False)
loop_options = (loop_1, loop_2, loop_3, loop_4)

def play_sound(sound, player: custom_types.Player, position=None):
    if G.EFFECT_VOLUME <= 0:
        return
    sound_player = pyglet.media.Player()

    try:
        driver = pyglet.media.drivers.silent.SilentAudioDriver
    except:
        #If the silent driver cannot be loaded, then sound is available
        try:
            listener = pyglet.media.get_audio_driver().get_listener()
            listener.volume = G.EFFECT_VOLUME
            listener.forward_orientation = player.get_sight_vector()
            if position:
                listener.position = player.position
                sound_player.position = position
            sound_player.queue(sound)
            sound_player.play()
            play_looping_sound(G.LAST_PLAYED_SONG)
        except:
            return sound_player

    return sound_player

def play_looping_sound(sound):
    try:
        driver = pyglet.media.drivers.silent.SilentAudioDriver
    except:
        looper = pyglet.media.SourceGroup(sound.audio_format, None)
        looper.loop = True
        looper.queue(sound)
        p = pyglet.media.Player()
        p.queue(looper)
        p.play()

