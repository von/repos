#!/usr/bin/env python
"""An example of subcommands with argparse """
from __future__ import print_function  # So we can get at print()

import os.path

import git

from Repo import Repo
from ReposCommand import ReposCommand


class AddCommand(ReposCommand):
    """Add one or more repos"""

    def get_parser(self, prog_name):
        parser = super(AddCommand, self).get_parser(prog_name)
        parser.add_argument('repo', nargs='*')
        return parser

    def take_action(self, parsed_args):
        assert(self.store is not None)
        repos = self.store.load()
        for repo in parsed_args.repo:
            try:
                r = Repo(os.path.expanduser(repo))
            except git.exc.InvalidGitRepositoryError:
                self.app.stdout.write("Not a repo: {}\n".format(repo))
                continue
            if r.working_dir in repos:
                self.app.stdout.write(
                    "Already in repos: {}\n".format(r.working_dir))
                continue
            self.app.stdout.write("Adding {}\n".format(r.working_dir))
            repos.append(r.working_dir)
        self.store.save(repos)
        return 0
