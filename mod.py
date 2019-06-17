# Imports, sorted alphabetically.

# Python packages
import importlib
import os
import sys

# Third-party packages
import pyglet

# Modules from this project
import globals as G
from debug import log_info

__all__ = ('load_modules')

def load_modules(server=False):
	mod_dir = pyglet.resource.get_settings_path("AstroCraft") + '\\mods'

	if not os.path.isdir(mod_dir):
		os.makedirs(mod_dir)

	sys.path.append(mod_dir)

	log_info('Mod loader has identified %d mods to load' % (len(os.listdir(mod_dir))))
	for name in os.listdir(mod_dir):
		module = importlib.import_module(name)
		module.initialize(server)
