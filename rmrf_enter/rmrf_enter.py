__version__ = "2015.11.03"
__author__ = "Luke Skibinski <l.skibinski@elifesciences.org"
__licence__ = "GPLv3"
__copyright__ = "eLife Sciences"
__description__ = """
`rmrf_enter.py` is a simple runner for scripts that describe which files they 
want to delete. 

Right now it's just deletables, but I might introduce other actions in the 
future.

see `example.py` for example usage of `rmrf_enter.py`"""

import os, re, shutil
from functools import wraps
from datetime import datetime, timedelta
import logging
from os.path import join

FORMAT = logging.Formatter("%(created)f - %(levelname)s - %(processName)s - %(name)s - %(message)s")
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# StreamHandler sends to stderr by default
HDLR = logging.StreamHandler()
HDLR.setFormatter(FORMAT)
LOG.addHandler(HDLR)

## common utils

def ymd(string):
    "extracts a standard yyyy-mm-dd value from given string or None"
    cregex = re.compile(r".*(?P<dt>\d{4}-\d{2}-\d{2}).*")
    matches = cregex.match(string)
    if matches:
        val = matches.groups()[0]
        try:
            return datetime.strptime(val, '%Y-%m-%d')
        except ValueError:
            msg = "ignoring filename that has matching YMD string BUT whose date cannot be parsed from it: %s"
            LOG.warn(msg, string)

def has_ymd_pattern(string, extractor_fn=ymd):
    "predicate. Returns True given extractor_fn can extract a value"
    return extractor_fn(string) != None

def older_than_N_days(fname, days=7, extractor_fn=ymd):
    """returns True if the value extractor from the filename
    is older than the given days value"""
    dtt = extractor_fn(fname)
    now = datetime.now()
    n_days_ago = timedelta(days=days)
    return dtt < (now - n_days_ago)

## actions

def delete(path):
    """delete action deletes a file or directory at the given path.
    if path is to a dir, contents are recursively deleted."""
    if os.path.isfile(path):
        LOG.debug("deleting FILE: " + path)
        return os.unlink(path)
    elif os.path.isdir(path):
        LOG.debug("deleting DIR : " + path)
        return shutil.rmtree(path)
    raise ValueError("cannot delete unhandled path type (??): %s" % path)

## do-er

def do_stuff(files_to_delete, dry_run=False):
    """given a list of triples (<action>, <dir root>, <predicate>)
    executes action on each file in dir if predicate"""
    supported_actions = {'delete': delete}

    def action_wrapper(action):
        @wraps(action)
        def fn(path):
            if dry_run:
                print 'dry run, skipping', path
                return
            LOG.info("%s path %s", action.__name__.upper(), path)
            return action(path)
        return fn

    for action_name, dir_root, fname_list_or_pickerfn in files_to_delete:
        assert action_name in supported_actions.keys(), "unspported action %r" % action_name
        action = action_wrapper(supported_actions[action_name])
        picker = fname_list = None
        dir_contents = sorted(os.listdir(dir_root))
        if callable(fname_list_or_pickerfn):
            picker = fname_list_or_pickerfn
            fname_list = filter(picker, dir_contents)
        else:
            fname_list = fname_list_or_pickerfn
        return [action(join(dir_root, fname)) for fname in fname_list]
