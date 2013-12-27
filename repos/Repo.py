#!/usr/bin/env python
# encoding: utf-8
"""Repo: wrapper around git.Repo"""

import git


class Repo(git.Repo):
    """Augmented git Repo object"""

    def needs_commit(self):
        """Return True if commit needed, False otherwise."""
        try:
            dirty = self.is_dirty
        except git.errors.GitCommandError:
            return False
        return dirty

    def needs_pull(self):
        """Return True if pull needed, False otherwise."""
        try:
            commits = self.commits_between("master", "origin")
        except git.errors.GitCommandError:
            return False
        behind = sum(1 for c in commits)
        return True if behind > 0 else False

    def needs_push(self):
        """Return True if push needed, False otherwise."""
        try:
            commits = self.commits_between("origin", "master")
        except git.errors.GitCommandError:
            return False
        ahead = sum(1 for c in commits)
        return True if ahead > 0 else False

    def status_string(self):
        """Return string describing repo status or None if nothing needed

        String will be comma-separate list of 'needs X' items.

        None means repo needs nothing."""
        attrs = []
        if self.needs_pull():
            attrs.append("needs pull")
        if self.needs_push():
            attrs.append("needs push")
        if self.needs_commit():
            attrs.append("needs commit")
        return ", ".join(attrs) if len(attrs) else None
