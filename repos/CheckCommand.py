#!/usr/bin/env python
"""CheckCommand object"""

import os
import Queue
import threading

import git

from CommandBase import CommandBase
from Repo import Repo


class CheckCommand(CommandBase):
    """Check all my repos"""

    def take_action(self, parsed_args):
        assert(self.store is not None)
        action_needed = False
        repos = self.store.load()
        threads = []
        queue = Queue.Queue()
        for repo in repos:
            try:
                r = Repo(os.path.expanduser(repo))
            except git.exc.InvalidGitRepositoryError:
                self.output("{}: Not a repo".format(repo))
                continue
            except git.exc.NoSuchPathError:
                self.output("{}: Does not exist".format(repo))
                continue
            t = threading.Thread(target=self.worker,
                                 args=(r, queue))
            threads.append(t)
            t.start()
        # Run until only main thread left
        while threading.active_count() > 1:
            try:
                response = queue.get(block=True, timeout=1)
            except Queue.Empty:
                # Timeout
                pass
            if response:
                print response
                action_needed = True
        return 1 if action_needed else 0

    def worker(self, repo, queue):
        """Get the status for a repo and put in queue if action needed."""
        self.log.debug("Checking {}".format(repo.working_dir))
        try:
            status = repo.status_string()
        except Exception as ex:
            self.output("Error checking {}: {}".format(
                repo.working_dir, str(ex)))
        else:
            if status:
                queue.put("{}: {}".format(repo.working_dir, status))
            else:
                queue.put(None)
