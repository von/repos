#!/usr/bin/env python
"""An example of subcommands with argparse """

import git

from CommandBase import CommandBase
from Repo import Repo


class NextCommand(CommandBase):
    """Output shell code to cd to next repo"""

    def take_action(self, parsed_args):
        assert(self.store is not None)
        repos = self.store.load()
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
                self.output("echo \"Done.\"")
                return 0
        self.output("cd {} && echo \"{}: {}\"\n".format(r.working_dir,
                                                        r.working_dir,
                                                        r.status_string()))
        return 0
