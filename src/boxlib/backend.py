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


from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

@singleton
class PutBoxBackend(object):

    def __init__(self):
        """ docstring """

    def list_files(self, user):
        text = os.listdir(localdir(user.name))
        return text

    def list_links(self, user):
        return LinkStore.findBy(owner=user.name)

    @inlineCallbacks
    def add_file(self, user, url, count, record):
        try:
            filename, mime, stream = record
            location = localdir(user.name, filename)
        except Exception, ex:
            log.err("Upload FAILED: %s" % ex.message)
            returnValue('Sorry. Something was wrong with your upload: %s' % ex.message)
        try:
            backend_rsp = self.write_file(stream, location)
        except Exception, ex:
            log.err("Upload FAILED: %s" % ex.message)
            returnValue('Sorry. Something went wrong saving your upload: %s' % ex.message)
        returnValue(backend_rsp)

    def write_file(self, stream, location):
        with open(location, 'w') as f:
            f.write(stream.read())
        log.msg('saved: %s' % location)
        return 'Upload to %s complete.' % location

    def remove_file(self, user, filename):
        return "Not really deleted: %s" % localdir(user.name, filename)

    @inlineCallbacks
    def add_link(self, user, file, url, count):
        try:
            db_record = yield LinkStore(
                    owner=user.name,
                    url=url,
                    file=file,
                    active=True,
                    get_limit=int(count),
                    get_count=0
                ).save()
        except Exception, ex:
            log.err("Upload FAILED: %s" % ex.message)
            returnValue('Sorry. The DB said: %s' % ex.message)
        returnValue("Link %s created." % url)

    def get_link(self, name):
        return LinkStore.findBy(
            url=name,
            #active=True
        ).addCallback(
            self.filterExpired
        )

    def filterExpired(self, lst):
        return filter(lambda r: r.get_count < r.get_limit, lst)


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
