#!/usr/bin/env python
"""An example of subcommands with argparse """
from __future__ import print_function  # So we can get at print()

import argparse
import os.path
import sys

import git

from App import RepoApp
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
        except git.exc.InvalidGitRepositoryError:
            output("Not a repo: {}".format(repo))
            continue
        if r.working_dir in repos:
            output("Already in repos: {}".format(r.working_dir))
            continue
        output("Adding {}".format(r.working_dir))
        repos.append(r.working_dir)
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
        except git.exc.InvalidGitRepositoryError:
            output("{}: Not a repo".format(repo))
            continue
        except git.exc.NoSuchPathError:
            output("{}: Does not exist".format(repo))
            continue
        debug("Checking {}".format(r.working_dir))
        status = r.status_string()
        if status:
            output("{}: {}".format(r.working_dir, status))
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
        except git.exc.InvalidGitRepositoryError:
            continue
        # We are in a git repo.
        # No need to go into subdirectories, so remove them
        del dirnames[:]
        if r.working_dir in repos:
            continue
        # We are in a git repo not registered and unseen.
        if args.add_new:
            output("Adding {}".format(r.working_dir))
            repos.append(r.working_dir)
            save_needed = True
        else:
            output(r.working_dir)
    if save_needed:
        store.save(repos)
    return 0


def next(args):
    """Find next repo that needs action

    Output shell code to cd to that repo and print status."""
    global store
    repos = store.load()
    # If we are in a repo that is in our list, find the next
    # Otherwise, we use the first
    try:
        r = Repo(".")
        i = repos.index(r.working_dir) + 1
        repos = repos[i:] + repos[:i]  # rotate i
        # Next repo is now is first position
    except git.exc.InvalidGitRepositoryError:
        # We're not in a repo
        pass
    except ValueError:
        # Repo we are in is not in repos
        pass
    # Find next repo with a status
    for repo in repos:
        try:
            r = Repo(repo)
        except git.exc.InvalidGitRepositoryError:
            continue
        status = r.status_string()
        if status:
            break
    else:
        output("Done.")
        return 0
    output("cd {} && echo \"{}: {}\"".format(r.working_dir,
                                             r.working_dir,
                                             r.status_string()))
    return 0

######################################################################
#
# Utility function

######################################################################


def main(argv=None):
    app = RepoApp()
    try:
        app.setup()
        app.run()
    finally:
        app.close()
    return 0  # XXX


def oldmain(argv=None):
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

    parser_next = subparsers.add_parser('next', help=next.__doc__)
    parser_next.set_defaults(func=next)

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
