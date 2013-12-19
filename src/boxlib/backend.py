from boxlib.logging import logwrapper as log
import os

def localdir(username, *args):
    p = ['files', username]
    p.extend(args)
    return os.path.sep.join(p)


instance = None
def singleton(cls):
    def wrapper():
        global instance
        if not instance:
            instance = cls()
        return instance
    return wrapper

@singleton
class PutBoxBackend(object):

    def __init__(self):
        """ docstring """

    def list_files(self, user):
        text = os.listdir(localdir(user.name))
        return text

    def list_links(self, user):
        return LinkStore.findBy(owner=user.name)

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

    def get_link(self, name):
        return LinkStore.findBy(url=name)


##
#  DB init
##

from twisted.enterprise import adbapi
from twistar.registry import Registry
from twisted.internet import reactor

from boxlib.setup import args

# Connect to the DB
SqliteRegistry = Registry(
    adbapi.ConnectionPool(
        'sqlite3',
        args.database
    )
)

from twistar.dbobject import DBObject

class LinkStore(DBObject):
    REGISTRY = SqliteRegistry
    TABLENAME = 'link_store'

#from twisted.internet import reactor

#def show(result):
    #log.msg("And it is... %s" % result)

#LinkStore.find(where=['id IS NOT NULL']).addCallback(show)
