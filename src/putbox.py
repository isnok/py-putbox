#!/usr/bin/env python

from argparse import ArgumentParser

parser = ArgumentParser(description="putbox launcher")

parser.add_argument(
        '-d', '--debug', default=False, action="store_true",
        help="debug flag (do not use in production :-)"
    )

args = parser.parse_args()

from boxlib.logging import logwrapper as log

if args.debug:
    log.msg("Startup args: %s" % vars(args))
