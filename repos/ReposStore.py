#!/usr/bin/env python
# encoding: utf-8
"""RepoStore: representation of storage for repository list"""

import os.path


class ReposStore(object):
    """Representation of storage for repository list"""

    def __init__(self, path):
        """Initialize store in given file path"""
        self._path = os.path.expanduser(path)

    def load(self):
        """Load my repos (list of paths as strings)."""
        if not os.path.exists(self._path):
            return []
        with open(os.path.expanduser(self._path)) as f:
            repos = [s.strip() for s in f.readlines()]
        return repos

    def save(self, repos):
        """Save my repos to given file."""
        with open(os.path.expanduser(self._path), "w") as f:
            map(f.write, [repo + "\n" for repo in repos])
