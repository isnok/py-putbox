from boxlib.setup import args
from boxlib.logging import logwrapper as log

##
#  Authentication Wrapper
##

from zope.interface import implements
from twisted.web2.auth.interfaces import IHTTPUser

class HTTPUser(object):
    implements(IHTTPUser)
    username = None
    def __init__(self, username):
        self.username = username

from twisted.cred.portal import IRealm

class LoginRealm(object):

    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IHTTPUser in interfaces:
            return IHTTPUser, HTTPUser(avatarId)
        raise NotImplementedError()


from twisted.web2.auth.digest import DigestCredentialFactory
from twisted.cred.checkers import FilePasswordDB
from twisted.cred.portal import Portal

portal = Portal(LoginRealm())
passwordDB = FilePasswordDB(args.passwordfile)
portal.registerChecker(passwordDB)

from twisted.web2.auth.wrapper import HTTPAuthResource
from boxlib.putzone import PutResource

put_guarded = HTTPAuthResource(
        PutResource(),
        [DigestCredentialFactory('md5', 'put_zone')],
        portal,
        (IHTTPUser,)
    )
