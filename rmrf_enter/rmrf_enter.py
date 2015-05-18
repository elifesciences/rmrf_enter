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

import os, re
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

## common utilities

def ymd(string):
    cregex = re.compile(r".*(?P<dt>\d{4}-\d{2}-\d{2}).*")
    matches = cregex.match(string)
    if matches:
        return matches.groups()[0]

def has_ymd_pattern(string):
    return ymd(string) != None

def older_than_N_days(fname, days=7):
    val = ymd(fname) # looks like: '2015-31-01'
    try:
        dt = datetime.strptime(val, '%Y-%m-%d')
        now = datetime.now()
        N_days_ago = timedelta(days=days)
        return dt < (now - N_days_ago)
    except ValueError:
        logger.warn("filename has a matching YMD string, but a date cannot be parsed from it: %s" % fname)


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
