#!/usr/bin/env python
"""Rm (remove) command"""

from CommandBase import CommandBase


class RmCommand(CommandBase):
    """Remove one or more repos"""

    def get_parser(self, prog_name):
        parser = super(RmCommand, self).get_parser(prog_name)
        parser.add_argument('repo', nargs='*')
        return parser

    def take_action(self, parsed_args):
        assert(self.store is not None)
        repos = self.store.load()
        needs_save = False
        for repo in parsed_args.repo:
            self.output("Removing {}".format(repo))
            try:
                repos.remove(repo)
            except ValueError:
                self.error("Repo not in list: {}".format(repo))
            else:
                needs_save = True
        if needs_save:
            self.store.save(repos)
        return 0
