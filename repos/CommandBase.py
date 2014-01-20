"""ReposCommand: base class for repos cliff Command classes"""

from __future__ import print_function  # So we can get at print()

import logging
import sys

from cliff.command import Command


class CommandBase(Command):
    """Base class for repos cliff Command classess"""

    log = logging.getLogger(__name__)

    @staticmethod
    def output(*args, **kwargs):
        """Output given message

        Arguments are to print()"""
        print(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        """Output given error message

        Arguments are to print()"""
        kwargs['file'] = sys.stderr
        print(*args, **kwargs)
