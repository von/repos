"""Cement App implementation for repos app"""

# TODO: How to handle command-specific arguments

import os

from cement.core import controller, foundation
import git

from Repo import Repo
from ReposStore import ReposStore


class RepoAppController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Manage git repos"

        config_defaults = dict(
            foo='bar',
            some_other_option='my default value',
        )

        arguments = [
            (['-r', '--repos_file'],
             dict(action='store',
                  default="~/.repos",
                  help='path to repos file'))
        ]

    @controller.expose(help="add a repository", hide=True)
    def default(self):
        """Display help"""
        pass  # XXX implement me

    @controller.expose(help="add a repository")
    def add(self):
        """Add repositories to monitor"""
        self.log.info("adding a repository")
        store = self._get_store()
        repos = store.load()
        for repo in self.pargs.repos:
            try:
                r = Repo(os.path.expanduser(repo))
            except git.exc.InvalidGitRepositoryError:
                self._output("Not a repo: {}".format(repo))
                continue
            if r.working_dir in repos:
                self._output("Already in repos: {}".format(r.working_dir))
                continue
            self._output("Adding {}".format(r.working_dir))
            repos.append(r.working_dir)
            store.save(repos)
            return 0

    @controller.expose(help="check repositories")
    def check(self):
        """Check repos for needed action"""
        self.log.info('check repositories')
        store = self._get_store()
        repos = store.load()
        action_needed = False
        self.log.debug("Loaded {} repos".format(len(repos)))
        for repo in repos:
            try:
                r = Repo(os.path.expanduser(repo))
            except git.exc.InvalidGitRepositoryError:
                self._output("{}: Not a repo".format(repo))
                continue
            except git.exc.NoSuchPathError:
                self._output("{}: Does not exist".format(repo))
                continue
            self.log.debug("Checking {}".format(r.working_dir))
            status = r.status_string()
            if status:
                self._output("{}: {}".format(r.working_dir, status))
                action_needed = True
                return 1 if action_needed else 0

    @controller.expose(help="find repositories")
    def find(self):
        """Find (and optionally add) any untracked repos"""
        store = self._get_store()
        repos = store.load()
        save_needed = False
        for dirpath, dirnames, filenames in os.walk(self.pargs.start_path):
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
            if self.pargs.add_new:
                self._output("Adding {}".format(r.working_dir))
                repos.append(r.working_dir)
                save_needed = True
            else:
                self._output(r.working_dir)
                if save_needed:
                    store.save(repos)
                    return 0

    @controller.expose(help="find repositories")
    def next(self):
        """Find next repo that needs action

        Output shell code to cd to that repo and print status."""
        store = self._get_store()
        repos = store.load()
        # If we are in a repo that is in our list, find the next
        # Otherwise, we use the first
        try:
            r = Repo(".")
            i = repos.index(r.working_dir) + 1
            repos = repos[i:] + repos[:i]  # rotate
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
                self._output("Done.")
                return 0
        self._output("cd {} && echo \"{}: {}\"".format(r.working_dir,
                                                       r.working_dir,
                                                       r.status_string()))
        return 0

    def _get_store(self):
        """Restore ReposStore object"""
        self.log.info(
            "Loading repos from {}".format(self.pargs.repos_file))
        store = ReposStore(self.pargs.repos_file)
        return store

    def _output(self, msg):
        """Output given message"""
        print(msg)


class RepoApp(foundation.CementApp):
    class Meta:
        label = 'RepoApp'
        base_controller = RepoAppController
