#!/usr/bin/env python3

"""Main XOInvader module, that is entry point to game.

Prepare environment for starting game and start it."""


import argparse
import logging

import xoinvader
from xoinvader.app import XOInvader


LOG = logging.getLogger(__name__)


def parse_args():
    """Parse incoming arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable debug mode"
    )

    args = parser.parse_args()
    return args


def main():
    """Start the game!"""

    args = parse_args()
    # apply settings to engine settings
    xoinvader.init(args.__dict__)
    LOG.debug("Incoming args: %s", args)
    game = XOInvader()
    return game.start()


if __name__ == "__main__":
    main()
