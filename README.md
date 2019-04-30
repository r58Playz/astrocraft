# astrocraft-python
This is the Python version of AstroCraft, a game like Minecraft.

Py3 support just started! Py2 has been dropped, as it reaches the end of its life on January 1, 2020.


### Dependencies

The dependencies are `pyglet`, `typing`, and `cython`. `typing` is included just in case the Python API drops support for typehints.

Install them using:
```
pip install pyglet
pip install typing
```

### Cython
```
pip install cython
python setup.py build_ext --inplace
```

This will generate .pyd files, which Python will prefer to load instead of your .py files, so you will need to rebuild or delete the .pyd each time you make changes.

setup.py will also compile Pyglet using Cython, if you download the pyglet source code and put the pyglet folder inside the game repository.

### Making your own builds for Windows

You can use setup.py to build `exe` files.

```
python setup.py build
```

This builds Cython-optimised `pyd` files, bundles all dependencies(including `Python`), and creates `exe` files.
