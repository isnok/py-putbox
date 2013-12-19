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

    def render(self, request):
        user = IAuthenticatedRequest(request).avatar
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
<form action="/upload?a=1&b=2&b=3" enctype="multipart/form-data" method="post">
    <input type="hidden" name="foo" value="bar">
    <input type="hidden" name="file_foo" value="not a file">
    file_foo: <input type="file" name="file_foo"><br/>
    file_foo: <input type="file" name="file_foo"><br/>
    file_bar: <input type="file" name="file_bar"><br/>
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
            print key
            for record in records:
                name, mime, stream = record
                data = stream.read()
                print '   %s %s %s %r' % (name, mime, stream, data)

        return Response(
            OK,
            {'content-type': MimeType('text', 'html')},
            stream='upload complete.'
        )
