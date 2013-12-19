from boxlib.logging import logwrapper as log

from twisted.web2.resource import Resource
from twisted.web2.http import Response
from twisted.web2.responsecode import OK
from twisted.web2.http_headers import MimeType

class GetResource(Resource):
    isLeaf = False

    def locateChild(self, req, segments):
        if segments:
            first = segments[0]
            log.msg("Get requested: %s" % first)
            return LanderPage(first), []
        else:
            return self, []

    def render(self, ctx):
        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream="You made it to the download zone!"
        )


class LanderPage(Resource):
    isLeaf = True

    def __init__(self, linkname):
        self.name = linkname

    def render(self, ctx):
        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream="You made it to the download link: %s" % self.name
        )
