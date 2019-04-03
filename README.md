# factories-python
This is based on ~bison--/Minecraft(https://github.com/bison--/Minecraft).

bison--/Minecraft is based on fogleman/Minecraft(https://github.com/fogleman/Minecraft)

Only runs on Python 2.7.

There's a branch for Python 3(still in development).

# Dependencies
Here are the dependencies:
- Pyglet
- Tkinter
- psutil
- colorama(https://github.com/tartley/colorama)

Tkinter comes installed with Python, and there is no other way to install it.
Here are the commands you need to run to install the dependencies:

```
pip install pyglet
pip install psutil
pip install colorama
```
# Running the game

To properly run the game, install Python 2.7 if you do not have it, install the dependencies(above), and run ```main.py```.

To use ```start.ps1```, you need to run the following commands before you can run it(we assume you have installed Python 2.7)

```
pip install pipenv
pipenv --python2.7
pipenv install pyglet
pipenv install psutil
pipenv install colorama
```

Then you can run ```start.ps1```
This does the same thing as above, but does it in a virtualenv instead of on the computer.
# Keyboard controls
W for forward

S for back

A for left

D for right

Space key to jump

R key to save

1 key to release mouse

Tab key to toggle flying

E key to chat

Q key to exit

# Goals
Our goals are:
save world,✓

load world,✓

has a educational use, and a use for fun, 

has a api(partly finished), 

be able to load each block's textures from different files,

Able to play multiplayer,

save and load worlds from online saves,

login with an account,

import worlds from Minecraft,

advanced gameplay,

more mobs than Minecraft,

mod interface,

npcs(non player charecters),

generated structures(villages, etc.),

generated water masses(lakes, oceans, rivers, etc.),

dimensions(land, sky, underworld, etc.),

be able to chat✓
