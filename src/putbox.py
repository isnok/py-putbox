#!/usr/bin/env python

from boxlib.setup import args
from boxlib.logging import logwrapper as log

if args.debug:
    log.msg("Startup args: %s" % vars(args))

from twisted.web2.resource import Resource
from boxlib.putting import put_guarded

main = Resource()
main.putChild('put', put_guarded)

from boxlib.getzone import GetResource
main.putChild('get', GetResource())

#from boxlib.putzone import UploadResource
#main.putChild('upload', UploadResource())


#from twisted.internet import reactor
#from twisted.web.server import Site

#reactor.listenTCP(args.port, Site(main), interface=args.interface)

from twisted.internet import reactor
from twisted.web2.server import Site
from twisted.web2.channel import HTTPFactory

reactor.listenTCP(args.port, HTTPFactory(Site(main)), interface=args.interface)

#def test(*args):
    #log.msg("test: %s" % (args,))
    #reactor.stop()
#reactor.callLater(3, test)

reactor.run()
