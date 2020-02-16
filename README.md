# astrocraft-python ![badge1](https://img.shields.io/badge/maintainance-not%20much-critical.svg) ![badge2](https://img.shields.io/badge/runnable-yes-success.svg) [![Build status](https://ci.appveyor.com/api/projects/status/413so98eyitcn9jx/branch/master?svg=true)](https://ci.appveyor.com/project/r58Playz/astrocraft-python/branch/master) [![codecov](https://codecov.io/gh/r58Playz/astrocraft-python/branch/master/graph/badge.svg)](https://codecov.io/gh/r58Playz/astrocraft-python)


This is the Python version of AstroCraft, a game like Minecraft.

Py3 support just started! Py2 has been dropped, as it reaches the end of its life on January 1, 2020.

A new formal website and download is going to be coming soon.


## Dependencies

The dependencies are `pyglet`, `typing`, and `cython`. `typing` is included just in case the Python API drops support for typehints.

Install them using `pip`:
```
pip install pyglet
pip install typing
pip install cython
```
* For Linux users: Install with `pip` **only** if the package manager does not support it. In some cases, you may not get support by them if installed with `pip`.

## Installation for Arch Linux

Use the PKGBUILD provided.
Note that plyer, a dependency, is not in the official repositories.

## Installation for Debian and other Debian based distros such as Ubuntu
Debian installation is difficult, as it involves enabling testing repositories.
Enable the testing repositories and update to Python 3.8.
Then download the latest version of AstroCraft:
```
git clone https://github.com/r58Playz/astrocraft-python.git astrocraft
```

Install pipenv:
```
sudo pip install pipenv
```
or install via ```apt```.

Now install dependencies:
```
cd astrocraft
pipenv shell
pipenv sync
```
Then run AstroCraft:
```
exit
pipenv run python main.py
```

Optionally, create a binary build of AstroCraft:
```
pipenv run python setup.py build
```
