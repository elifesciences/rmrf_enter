__version__ = "2015.05.06"
__author__ = "Luke Skibinski <l.skibinski@elifesciences.org"
__licence__ = "GPLv3"
__copyright__ = "eLife Sciences"
__description__ = """
`rmrf_enter.py` is a simple runner for scripts that describe which files they 
want to delete. 

Right now it's just deletables, but I might introduce other actions in the 
future.

see `example.py` for example usage of `rmrf_enter.py`"""

import os

## actions

def delete(path):
    if os.path.isfile(path):
        return os.unlink(path)
    raise ValueError("we only delete individual files right now!")

## do-er

def do_stuff(files_to_delete):
    for action, dir_root, picker in files_to_delete:
        for fname in os.listdir(dir_root):
            if picker(fname):
                print(action + ": " + fname)
                eval(action)(os.path.join(dir_root, fname))
