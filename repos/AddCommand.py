#!/usr/bin/env python
"""An example of subcommands with argparse """

import os.path

import git

from CommandBase import CommandBase
from Repo import Repo


class AddCommand(CommandBase):
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
                self.error("Not a repo: {}".format(repo))
                continue
            if r.working_dir in repos:
                self.output("Already in repos: {}".format(r.working_dir))
                continue
            self.output("Adding {}".format(r.working_dir))
            repos.append(r.working_dir)
        self.store.save(repos)
        return 0
