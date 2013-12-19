from boxlib.logging import logwrapper as log

##
#  PutZone Resource
##

from twisted.web2.resource import Resource
from twisted.web2.auth.interfaces import IAuthenticatedRequest
from twisted.web2.http import Response
from twisted.web2.responsecode import OK
from twisted.web2.http_headers import MimeType

class PutResource(Resource):
    isLeaf = True

    #def __init__(self, user):
        #self.user = user

    def render(self, ctx):
        user = IAuthenticatedRequest(ctx).avatar
        text = [ "Hello %s." % user.name, "Welcome to the put-Zone!" ]
        text.extend(self.render_files())
        text.extend(self.render_links())
        text.extend(self.mk_link_form())
        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='<br>'.join(text)
        )

    def render_files(self):
        return []

    def render_links(self):
        return []

    def mk_link_form(self):
        return ["""
<form action="/upload" enctype="multipart/form-data" method="post">
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
        for key, vals in request.args.iteritems():
            for val in vals:
                print key, val

        log.msg('file uploads ----------------')
        for key, records in request.files.iteritems():
            log.msg("Received as %s:" % key)
            for record in records:
                name, mime, stream = record
                data = stream.read()
                with open('files/test/%s' % name, 'w') as f:
                    f.write(data)
                log.msg('got: %s %s %s %r' % (name, mime, stream, data))

        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='upload complete.'
        )
