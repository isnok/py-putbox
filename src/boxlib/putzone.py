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

class PutResource(Resource):
    isLeaf = True

    def __init__(self):
        self.putChild('upload', UploadResource())
        self.putChild('delete', DeleteResource())
        self.backend = PutBoxBackend()

    def render(self, ctx):
        user = IAuthenticatedRequest(ctx).avatar
        text = [ "Hello %s." % user.name, "Welcome to the put-Zone!", '' ]
        text.extend(self.render_files(user))
        text.extend(self.render_links(user))
        text.extend(self.mk_link_form())
        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='<br>'.join(text)
        )

    def render_file(self, filename):
        return '%s <a href="/put/delete?file=%s">delete</a>' % (filename, filename)

    def render_files(self, user):
        text = [ "Files of user %r:" % user.name ]
        raw_list = self.backend.list_files(user)
        text.extend(map(self.render_file, raw_list))
        text.append('')
        return text

    def render_links(self, user):
        text = [ "Links of user %r:" % user.name ]
        text.extend(self.backend.list_links(user))
        text.append('')
        return text

    def mk_link_form(self):
        return ["""
<form action="/put/upload" enctype="multipart/form-data" method="post">
    Choose a file to upload: <input type="file" name="putted"><br/>
    <input type="submit" value="submit">
</form>
        """]


from twisted.web2.iweb import IRequest
from twisted.web2.http import Response
from twisted.web2.resource import PostableResource

class UploadResource(PostableResource):

    def render(self, ctx):
        request = IRequest(ctx)

        log.msg('---------------- file upload ----------------')
        for key, records in request.files.iteritems():
            log.msg("Received as %s:" % key)
            for record in records:
                name, mime, stream = record
                with open('files/test/%s' % name, 'w') as f:
                    f.write(stream.read())
                log.msg('saved: %s %s' % (name, mime))

        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='Upload complete. <a href="/put">Go back to PutZone.</a>'
        )

class DeleteResource(Resource):

    def render(self, ctx):
        request = IRequest(ctx)
        filename = request.args['file'][0]

        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='File deleted: %s <a href="/put">Go back to PutZone.</a>' % filename
        )
