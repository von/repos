#!/usr/bin/env python
# encoding: utf-8
"""Repo: wrapper around git.Repo"""

import logging

import git


class Repo(git.Repo):
    """Augmented git Repo object"""

    log = logging.getLogger(__name__)

    def needs_commit(self):
        """Return True if commit needed, False otherwise."""
        try:
            dirty = self.is_dirty()
        except git.exc.GitCommandError:
            return False
        return dirty

    def commits_behind_remote(self):
        """Return the number of commmits we are behind our remote."""
        master = "master"
        remote = "{}/master".format(self.remote())
        self._debug(
            "commits_behind_remote(): Checking between {} and {}".format(
                master, remote))
        commit_count = self.commit_count_between(master, remote)
        return commit_count

    def commits_ahead_of_remote(self):
        """Return the number of commmits we are ahead of our remote."""
        master = "master"
        remote = "{}/master".format(self.remote())
        self._debug(
            "commits_ahead_of_remote(): Checking between {} and {}".format(
                remote, master))
        commit_count = self.commit_count_between(remote, master)
        return commit_count

    def commit_count_between(self, from_name, to_name):
        """Return number of commits from one refence name to another.

        For example: r.commmit_count_between("master", "origin/master")"""
        commits = self.iter_commits("{}..{}".format(from_name, to_name))
        count = sum(1 for c in commits)
        return count

    def status_string(self):
        """Return string describing repo status or None if nothing needed

        String will be comma-separate list of 'needs X' items.

        None means repo needs nothing."""
        attrs = []
        pull_commit_count = self.commits_behind_remote()
        if pull_commit_count:
            attrs.append("needs pull({})".format(pull_commit_count))
        push_commit_count = self.commits_ahead_of_remote()
        if push_commit_count:
            attrs.append("needs push({})".format(push_commit_count))
        if self.needs_commit():
            attrs.append("needs commit")
        return ", ".join(attrs) if len(attrs) else None

    def _debug(self, msg):
        """Handle a debugging message."""
        self.log.debug(msg)
