"""ReposCommand: base class for repos cliff Command classes"""

import logging

from cliff.command import Command


class ReposCommand(Command):
    """Base class for repos cliff Command classess"""

    log = logging.getLogger(__name__)
