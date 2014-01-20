#!/usr/bin/env python
"""CheckCommand object"""

import os

import git

from CommandBase import CommandBase
from Repo import Repo


class CheckCommand(CommandBase):
    """Check all my repos"""

    def take_action(self, parsed_args):
        assert(self.store is not None)
        action_needed = False
        repos = self.store.load()
        for repo in repos:
            try:
                r = Repo(os.path.expanduser(repo))
            except git.exc.InvalidGitRepositoryError:
                self.output("{}: Not a repo".format(repo))
                continue
            except git.exc.NoSuchPathError:
                self.output("{}: Does not exist".format(repo))
                continue
            self.log.debug("Checking {}".format(r.working_dir))
            status = r.status_string()
            if status:
                self.output("{}: {}".format(r.working_dir, status))
                action_needed = True
        return 1 if action_needed else 0
