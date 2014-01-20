#!/usr/bin/env python
"""check Command for repors"""
from __future__ import print_function  # So we can get at print()

import os

import git

from Repo import Repo
from ReposCommand import ReposCommand


class CheckCommand(ReposCommand):
    """Check all my repos"""

    def take_action(self, parsed_args):
        assert(self.store is not None)
        action_needed = False
        repos = self.store.load()
        for repo in repos:
            try:
                r = Repo(os.path.expanduser(repo))
            except git.exc.InvalidGitRepositoryError:
                self.app.stdout.write("{}: Not a repo\n".format(repo))
                continue
            except git.exc.NoSuchPathError:
                self.app.stdout.write("{}: Does not exist\n".format(repo))
                continue
            self.log.debug("Checking {}".format(r.working_dir))
            status = r.status_string()
            if status:
                self.app.stdout.write("{}: {}\n".format(r.working_dir,
                                                        status))
                action_needed = True
        return 1 if action_needed else 0
