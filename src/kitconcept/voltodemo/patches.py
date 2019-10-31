from .interfaces import IVoltoSettings
from plone.registry.interfaces import IRegistry
from plone.rest.interfaces import IAPIRequest
from zope.component import getUtility

def construct_url(self, randomstring):
    """Return URL used in registered_nodify_template to allow user to 
       change password
    """
    # domain as seen by Plone backend
    frontend_domain = self.portal_state().navigation_root_url()
    if IAPIRequest.providedBy(self.request):
        # the reset was requested through restapi, the frontend might have
        # a different domain. Use volto.frontend_domain in the registry
        # without triggering possible "record not found"
        # Default value for volto.frontend_domain is http://localhost:3000

        # to consider: maybe we should/could override @@portal_state/navigation_root_url() for
        # IAPIRequest to fix this on a higher level

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IVoltoSettings, prefix="volto", check=False)
        frontend_domain = getattr(settings, "frontend_domain", frontend_domain)
        if frontend_domain.endswith('/'):
            frontend_domain = frontend_domain[:-1]
    return "%s/passwordreset/%s" % (frontend_domain, randomstring)
