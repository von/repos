#!/usr/bin/env python
"""An example of subcommands with argparse """
from __future__ import print_function  # So we can get at print()

import sys


from App import ReposApp


def main(argv=None):
    argv = argv if argv else sys.argv[1:]
    myapp = ReposApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main())
