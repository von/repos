#!/usr/bin/env python
"""An example of subcommands with argparse """
from __future__ import print_function  # So we can get at print()

import os.path

import git

from Repo import Repo
from ReposCommand import ReposCommand


class FindCommand(ReposCommand):
    """Find repos not currently monitored"""

    def get_parser(self, prog_name):
        parser = super(FindCommand, self).get_parser(prog_name)
        parser.add_argument("-a", "--add_new",
                            action="store_true", default=False,
                            help="automatically add new repos")
        parser.add_argument("start_path", default=".", nargs="?",
                            help="path to start search", metavar="path")
        return parser

    def take_action(self, parsed_args):
        assert(self.store is not None)
        repos = self.store.load()
        save_needed = False
        for dirpath, dirnames, filenames in \
                os.walk(parsed_args.start_path):
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
            if parsed_args.add_new:
                self.app.stdout.write("Adding {}\n".format(r.working_dir))
                repos.append(r.working_dir)
                save_needed = True
            else:
                self.app.stdout.write("{}\n".format(r.working_dir))
        if save_needed:
            self.store.save(repos)
        return 0
