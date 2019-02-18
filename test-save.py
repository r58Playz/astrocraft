from main import *
from saveLoad import saveLoad

def test_save():
    window = Window(width=800, height=600, caption='Pyglet', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()
    loc = (0,0,0)
    model = window.model
    model.add_block(loc, GRASS)
    model.show_block(loc)
    saveload = saveLoad()
    saveload.saveWorld(model,"SAVE.FACTORIES")

if __name__ == '__main__':
    test_save()