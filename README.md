# astrocraft-python
This is the Python version of AstroCraft, a game like Minecraft.

Py3 support just started! Py2 has been dropped, as it reaches the end of its life on January 1, 2020.


### Dependencies

The dependencies are `pyglet`, `typing`, and `cython`. `typing` is included just in case the Python API drops support for typehints.

Install them using:
```
pip install pyglet
pip install typing
pip install cython
```

### Making your own installer or build for Windows

You can use PyInstaller(https://github.com/pyinstaller/pyinstaller) to build a one-folder build. 

```
pyinstaller main.spec
```

Extensive documentation for PyInstaller is available at https://pyinstaller.readthedocs.io/en/stable/

Then you can use FreeExtractor (https://sourceforge.net/projects/freeextractor/) to build a installer for AstroCraft.

You can install PyInstaller with administrator priveleges to get system-wide commands.

```
pip install PyInstaller
```

Otherwise you will need to invoke `pyinstaller.py` to use PyInstaller.
