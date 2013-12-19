#!/usr/bin/env python

from boxlib.setup import args
from boxlib.logging import logwrapper as log

if args.debug:
    log.msg("Startup args: %s" % vars(args))

from twisted.internet import reactor
from twisted.web.server import Site


def test(*args):
    log.msg("test: %s" % (args,))
    reactor.stop()


reactor.callLater(3, test)
reactor.run()
