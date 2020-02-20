import glob
import os
import sys

from Cython.Distutils import build_ext
from distutils.util import get_platform
from distutils.extension import Extension

import globals as G


excluded_modules = (
    'globals',
    'gui',
    'views',
    'controllers',
    'mods',
    'build',
    'setup',
    'setup-py2exe',
    'setup-cx_Freeze',
    'pyglet.gl.glext_arb',
    'pyglet.gl.glext_nv',
    'pyglet.image.codecs',
    'pyglet.image.codecs.pypng',
    'pyglet.media',
    'pyglet.media.drivers.alsa.asound',
    'pyglet.window',
    'pyglet.window.xlib.xlib',
    'venv',
)

excluded_includes = (
    'main',
    'manager',
)


def find_files(source, target, patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source, pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
    return sorted(ret.items())


def get_modules(path=None):
    first = False
    if path is None:
        path = os.path.abspath(os.path.dirname(__file__))
        first = True
    for f_or_d in os.listdir(path):
        if not first:
            f_or_d = os.path.join(path, f_or_d)
        if os.path.isdir(f_or_d) and f_or_d not in excluded_modules:
            d = f_or_d
            for name, f in get_modules(d):
                yield name, f
        else:
            f = f_or_d
            if f.endswith(('.py', 'pyx')):
                name = '.'.join(s for s in f.split('.')[0].replace("\\","/").split('/')
                                if s != '__init__')
                if name and name not in excluded_modules:
                    yield name, f


ext_modules = [Extension(name, [f]) for name, f in get_modules()]
includes = [name for name, f in get_modules() if name not in excluded_includes]

packages = ["pyglet", "sqlite3"]  # force cx_Freeze to bundle these

cython_output_dir = "build/cython"
options = {
    'build_ext': {
        # 'inplace': True,
        'cython_c_in_temp': True,
        'cython_directives': {
            'language_level': '3',
        }
    },
}

if len(sys.argv) > 1 and sys.argv[1] in ("build", "build_exe"):
    from cx_Freeze import setup, Executable

    options['build_exe'] = {
        'packages': packages,
        'excludes': ['test', 'unittest'],
        'includes': includes,
        'include_files': ['resources/'],
        "path": [cython_output_dir] + sys.path,
    }
    executables = [Executable("main.py", targetName=G.APP_NAME + (".exe" if sys.platform == 'win32' else '')),
                   Executable("server.py"), Executable("update.py")]

else:
    from distutils.core import setup

    executables = []

setup(
    name=G.APP_NAME,
    cmdclass={'build_ext': build_ext},
    options=options,
    requires=['pyglet', 'Cython'],
    version=G.APP_VERSION,
    description="",
    ext_modules=ext_modules,
    executables=executables,
)
