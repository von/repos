#!/usr/bin/env python
"""An example of subcommands with argparse """
from __future__ import print_function  # So we can get at print()

import argparse
import os.path
import sys

import git

from Repo import Repo
from ReposStore import ReposStore

######################################################################
#
# Globals

# Output functions
output = print


# Debug output
def debug(m):
    """Output a debug message. Does nothing by default."""
    pass

# ReposStore
store = None

######################################################################
#
# Subcommands


def add(args):
    """Add one or more repos"""
    global store
    repos = store.load()
    for repo in args.repo:
        try:
            r = Repo(os.path.expanduser(repo))
        except git.InvalidGitRepositoryError:
            output("Not a repo: {}".format(repo))
            continue
        if r.wd in repos:
            output("Already in repos: {}".format(r.wd))
            continue
        output("Adding {}".format(r.wd))
        repos.append(r.wd)
    store.save(repos)
    return 0


def check(args):
    """Check all my repos"""
    global store
    action_needed = False
    repos = store.load()
    debug("Loaded {} repos".format(len(repos)))
    for repo in repos:
        try:
            r = Repo(os.path.expanduser(repo))
        except git.InvalidGitRepositoryError:
            output("{}: Not a repo".format(repo))
            continue
        debug("Checking {}".format(r.wd))
        status = r.status_string()
        if status:
            output("{}: {}".format(r.wd, status))
            action_needed = True
    return 1 if action_needed else 0


def find(args):
    """Find (and optionally add) any untracked repos"""
    global store
    repos = store.load()
    save_needed = False
    for dirpath, dirnames, filenames in os.walk(args.start_path):
        try:
            r = Repo(dirpath)
        except git.InvalidGitRepositoryError:
            continue
        # We are in a git repo.
        # No need to go into subdirectories, so remove them
        del dirnames[:]
        if r.wd in repos:
            continue
        # We are in a git repo not registered and unseen.
        if args.add_new:
            output("Adding {}".format(r.wd))
            repos.append(r.wd)
            save_needed = True
        else:
            output(r.wd)
    if save_needed:
        store.save(repos)
    return 0


######################################################################
#
# Utility function

######################################################################


def main(argv=None):
    # Do argv default this way, as doing it in the functional
    # declaration sets it at compile time.
    if argv is None:
        argv = sys.argv

    # Argument parsing
    parser = argparse.ArgumentParser(
        description=__doc__,  # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # To have --help print defaults with trade-off it changes
        # formatting, use: ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-r", "--repos_file", default="~/.repos",
                        help="Specify path to repos file",
                        metavar="path")
    parser.add_argument("-v", "--verbose",
                        action="store_true", default=False,
                        help="verbose mode")
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_add = subparsers.add_parser('add', help=add.__doc__)
    parser_add.set_defaults(func=add)
    parser_add.add_argument("repo", nargs="+",
                            help="add repos to track", metavar="repo")

    parser_check = subparsers.add_parser('check', help=check.__doc__)
    parser_check.set_defaults(func=check)

    parser_find = subparsers.add_parser('find', help=find.__doc__)
    parser_find.set_defaults(func=find)
    parser_find.add_argument("-a", "--add_new",
                             action="store_true", default=False,
                             help="automatically add new repos")
    parser_find.add_argument("start_path", default=".", nargs="?",
                             help="path to start search", metavar="path")

    args = parser.parse_args()

    if args.verbose:
        global debug
        debug = output

    global store
    store = ReposStore(args.repos_file)

    func = args.func
    status = func(args)
    return status

if __name__ == "__main__":
    sys.exit(main())
