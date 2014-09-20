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
            if self.print_repo_status(r):
                action_needed = True
        return 1 if action_needed else 0

    def print_repo_status(self, repo):
        """Print the status for a repo if action needed.

        Returns True if action needed, false otherwise."""
        self.log.debug("Checking {}".format(repo.working_dir))
        try:
            status = repo.status_string()
        except Exception as ex:
            self.output("Error checking {}: {}".format(
                repo.working_dir, str(ex)))
            action_needed = False
        else:
            if status:
                self.output("{}: {}".format(repo.working_dir, status))
                action_needed = True
            else:
                action_needed = False
        return action_needed
