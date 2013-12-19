from boxlib.logging import logwrapper as log
import os

def localdir(username, *args):
    p = ['files', username]
    p.extend(args)
    return os.path.sep.join(p)

class PutBoxBackend(object):

    def __init__(self):
        """ docstring """

    def list_files(self, user):
        text = os.listdir(localdir(user.name))
        return text

    def list_links(self, user):
        text = [ "No links up to now." ]
        return text

    def add_file(self, user, record):
        try:
            filename, mime, stream = record
            with open(localdir(user.name, filename), 'w') as f:
                f.write(stream.read())
            log.msg('saved: %s' % localdir(user.name, filename))
            return 'Upload of %s complete.' % filename
        except Exception, ex:
            log.err("Upload FAILED: %s" % ex.message)
            return 'Sorry. Something went wrong while saving your upload: %s' % ex.message

    def remove_file(self, user, filename):
        return "Not really deleted: %s" % localdir(user.name, filename)

