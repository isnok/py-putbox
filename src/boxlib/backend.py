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

    def remove_file(self, user, filename):
        return "Not really deleted: %s" % localdir(user.name, filename)

