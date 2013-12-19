from boxlib.logging import logwrapper as log

##
#  PutZone Resource
##

from twisted.web2.resource import Resource
from twisted.web2.auth.interfaces import IAuthenticatedRequest
from twisted.web2.http import Response
from twisted.web2.responsecode import OK
from twisted.web2.http_headers import MimeType

from boxlib.backend import PutBoxBackend

from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

from boxlib.helpers import rndname

class PutResource(Resource):
    isLeaf = True

    def __init__(self):
        self.putChild('upload', UploadResource())
        self.putChild('delete', DeleteResource())
        self.putChild('link', LinkResource())
        self.backend = PutBoxBackend()

    @inlineCallbacks
    def render(self, ctx):
        user = IAuthenticatedRequest(ctx).avatar
        text = [ "Hello %s." % user.name, "Welcome to the put-Zone!", '' ]
        text.extend(self.render_files(user))
        links = yield self.render_links(user)
        text.extend(links)
        text.extend(self.mk_link_form())
        returnValue(
            Response(
                OK,
                {'content-type': MimeType('text', 'html')},
                stream='<br>'.join(text)
            )
        )

    def render_file(self, filename):
        return '%s <a href="/put/delete?file=%s">delete</a>' % (filename, filename)

    def render_files(self, user):
        text = [ "Files of user %r:" % user.name ]
        raw_list = self.backend.list_files(user)
        text.extend(map(self.render_file, raw_list))
        text.append('')
        return text

    def render_link(self, link):
        ''' we get unicode from the twistar object, but need str '''
        formatted = 'Link: <a href="/get/%(url)s">%(url)s</a> (limit: %(get_limit)s, downloaded: %(get_count)s)' % vars(link)
        return str(formatted)

    @inlineCallbacks
    def render_links(self, user):
        text = [ "Links of user %r:" % user.name ]
        raw_links = yield self.backend.list_links(user)
        text.extend(map(self.render_link, raw_links))
        text.append('')
        returnValue(text)

    def mk_link_form(self):
        return ["""
Upload a file:
<form action="/put/upload" enctype="multipart/form-data" method="post">
    Choose a file to upload: <input type="file" name="putted"><br/>
    <input type="submit" value="submit">
</form>
Create a link:
<form action="/put/link" enctype="multipart/form-data" method="post">
    Uploaded file name: <input type="text" name="file"><br/>
    Set a download url: <input type="text" name="url" value="%s"><br />
    Set a download count: <input type="text" name="get_count" value="30"><br />
    <input type="submit" value="submit">
</form>
        """ % rndname(18,22)]


from twisted.web2.iweb import IRequest
from twisted.web2.http import Response
from twisted.web2.resource import PostableResource

class UploadResource(PostableResource):

    def __init__(self):
        self.backend = PutBoxBackend()

    @inlineCallbacks
    def render(self, ctx):
        request = IRequest(ctx)
        user = IAuthenticatedRequest(ctx).avatar

        log.msg('---------------- file upload ----------------')
        for formkey, records in request.files.iteritems():
            #log.msg("Received as %s:" % formkey)
            for record in records:
                backend_rsp = yield self.backend.add_file(user, link_url, get_count, record)

        returnValue(
            Response(
                OK,
                {'content-type': MimeType('text', 'html')},
                stream='%s<br><a href="/put">Go back to PutZone.</a>' % backend_rsp
            )
        )


class DeleteResource(Resource):

    def __init__(self):
        self.backend = PutBoxBackend()

    def render(self, ctx):
        request = IRequest(ctx)
        filename = request.args['file'][0]
        user = IAuthenticatedRequest(ctx).avatar
        backend_rsp = self.backend.remove_file(user, filename)

        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='%s<br><a href="/put">Go back to PutZone.</a>' % backend_rsp
        )


class LinkResource(PostableResource):

    def __init__(self):
        self.backend = PutBoxBackend()

    @inlineCallbacks
    def render(self, ctx):
        request = IRequest(ctx)
        user = IAuthenticatedRequest(ctx).avatar

        file = request.args['file'][0]
        url = request.args['url'][0]
        get_count = request.args['get_count'][0]

        log.msg('---------------- link create ----------------')
        backend_rsp = yield self.backend.add_link(user, file, url, get_count)

        returnValue(
            Response(
                OK,
                {'content-type': MimeType('text', 'html')},
                stream='%s<br><a href="/put">Go back to PutZone.</a>' % backend_rsp
            )
        )
