# -*- coding: utf-8 -*-
from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import aq_parent
from plone import api
from Products.CMFCore.permissions import ManagePortal
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin  # noqa
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.interface import implements


manage_addJWTCookieAuthPlugin = PageTemplateFile(
    "add_plugin", globals(), __name__="manage_addJWTCookieAuthPlugin")


def addJWTCookieAuthPlugin(self, id_, title=None, REQUEST=None):
    """Add a JWT authentication plugin
    """
    plugin = JWTCookieAuthPlugin(id_, title)
    self._setObject(plugin.getId(), plugin)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace"
            "?manage_tabs_message=JWT+cookie+auth+plugin+added." %
            self.absolute_url()
        )


class JWTCookieAuthPlugin(BasePlugin):
    """Plone PAS plugin for authentication with JSON web tokens (JWT) embedded
    in a cookie.
    """
    implements(
        IAuthenticationPlugin,
        IExtractionPlugin,
    )
    meta_type = "JWT Cookie Auth Plugin"
    security = ClassSecurityInfo()

    token_timeout = 60 * 60 * 12  # 12 hours
    use_keyring = True
    store_tokens = False
    _secret = None
    _tokens = None

    # ZMI tab for configuration page
    manage_options = (
        ({'label': 'Configuration',
          'action': 'manage_config'},) +
        BasePlugin.manage_options
    )
    security.declareProtected(ManagePortal, 'manage_config')
    manage_config = PageTemplateFile('config', globals(),
                                     __name__='manage_config')

    def __init__(self, id_, title=None):
        self._setId(id_)
        self.title = title

    security.declarePrivate('extractCredentials')

    # IExtractionPlugin implementation
    # Extracts a JSON web token from the cookie.
    def extractCredentials(self, request):
        creds = {}
        cookie = request.cookies.get('auth_token', None)
        if cookie is None:
            return None

        creds['token'] = cookie

        return creds

    security.declarePrivate('authenticateCredentials')

    # IAuthenticationPlugin implementation
    def authenticateCredentials(self, credentials):
        # Ignore credentials that are not from our extractor
        extractor = credentials.get('extractor')
        if extractor != self.getId():
            return None

        pas = self._getPAS()

        jwt_plugin = pas.get('jwt_auth', False)

        if not jwt_plugin:
            return None

        payload = jwt_plugin._decode_token(credentials['token'])
        if not payload:
            # Not found in local jwt_auth plugin, let's try in root Zope's one
            # This enables Zope's admin access (just for convenience)
            try:
                portal = api.portal.get()
                jwt_auth_parent = aq_parent(portal).acl_users.jwt_auth
                payload = jwt_auth_parent._decode_token(credentials['token'])
            except:  # noqa
                return None

            if not payload:
                return None

        if 'sub' not in payload:
            return None

        userid = payload['sub'].encode('utf8')

        if jwt_plugin.store_tokens:
            if userid not in jwt_plugin._tokens:
                return None
            if credentials['token'] not in jwt_plugin._tokens[userid]:
                return None

        return (userid, userid)
