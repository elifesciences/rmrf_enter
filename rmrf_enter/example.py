__author__ = "Luke Skibinski <l.skibinski@elifesciences.org"
__licence__ = "GPLv3"
__copyright__ = "eLife Sciences"
__description__ = "example usage of rmrf_enter.py"

import os

def looks_funny(fname):
    "returns `True` if the sub string 'harhar' is found in the given filename"
    return "harhar" in fname

def files_to_delete():
    """a list of triplets of `action`, `directory`, and a callable
    that returns True if the action should be performed on that file."""
    return [
        # this triplet will delete all files in the /tmp/ directory whose 
        # filename contains the substring "harhar"
        ("delete", "/tmp/", lambda fname: looks_funny(fname)),
    ]

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

if __name__ == '__main__':
    import rmrf_enter
    touch("/tmp/fooharharbar")
    os.mkdir("/tmp/barharharfoo")
    touch("/tmp/barharharfoo/baz")
    rmrf_enter.do_stuff(files_to_delete())
