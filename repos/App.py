"""Cliff App implementation for repos app"""

import logging

from cliff.app import App
from cliff.commandmanager import CommandManager

from ReposStore import ReposStore


class ReposApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(ReposApp, self).__init__(
            description='repos: monitor git repositories',
            version='0.1',
            command_manager=CommandManager('repos'),
        )

    def build_option_parser(self, description, version, argparse_kwargs=None):
        self.log.debug('build_option_parser')
        parser = super(ReposApp, self).build_option_parser(description,
                                                           version,
                                                           argparse_kwargs)
        parser.add_argument("-r", "--repos_file", default="~/.repos",
                            help="Specify path to repos file",
                            metavar="path")
        return parser

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
        self.log.debug("argv: {}".format(",".join(argv)))

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        self.log.debug(
            "Loading repos from {}".format(self.options.repos_file))
        cmd.store = ReposStore(self.options.repos_file)

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)
