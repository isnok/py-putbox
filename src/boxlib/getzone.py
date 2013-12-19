from boxlib.logging import logwrapper as log

from twisted.web2.resource import Resource
from twisted.web2.http import Response
from twisted.web2.responsecode import OK
from twisted.web2.http_headers import MimeType

class GetResource(Resource):
    isLeaf = False

    def locateChild(self, req, segments):
        if segments:
            first = segments.pop(0)
            log.msg("Get requested: %s" % first)
            return LanderPage(first), segments
        else:
            return self, []

    def render(self, ctx):
        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream="You made it to the download zone!"
        )


from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue
from boxlib.backend import PutBoxBackend

class LanderPage(Resource):
    isLeaf = False

    def __init__(self, linkname):
        self.name = linkname
        self.backend = PutBoxBackend()

    def locateChild(self, req, segments):
        if segments:
            first = segments[0]
            log.msg("Download requested: %s" % first)
            return CountedDownload(self.name), []
        return self, []

    @inlineCallbacks
    def render(self, ctx):
        text = "You made it to the download link: %s" % self.name
        content_here = yield self.backend.get_link(self.name)
        if content_here:
            filename = content_here[0].file
            text += '<br>You can now download the file:<br><a href="/get/%s/%s">%s</a>' % (self.name, filename, filename)
        else:
            text += "<br>Sorry this link is dead."

        returnValue(
            Response(
                OK,
                {'content-type': MimeType('text', 'html')},
                stream=str(text)
            )
        )


from twisted.web2.stream import FileStream

class CountedDownload(Resource):

    def __init__(self, linkname):
        self.name = linkname
        self.backend = PutBoxBackend()

    @inlineCallbacks
    def render(self, ctx):
        okToDownload, filename = yield self.backend.increaseCount(self.name)
        if okToDownload:
            log.msg("OK to download %r: %s" % (filename, okToDownload))
            mime =  MimeType('application', 'octet-stream')
            returnStream = FileStream(open(filename, 'r'))
        else:
            log.msg("Not OK to download: %s" % okToDownload)
            mime = MimeType('text', 'html')
            returnStream = 'Sorry, the link is expired.'

        returnValue(
            Response(
                OK,
                { 'content-type': mime },
                stream=returnStream
            )
        )

