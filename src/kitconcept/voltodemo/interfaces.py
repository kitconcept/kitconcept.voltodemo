# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IKitconceptvoltodemoCoreLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IHomepage(model.Schema):
    """ Homepage content type interface
    """


class IVoltoSettings(Interface):
    """ Volto settings necessary to store ont he backend
    """

    frontend_domain = schema.URI(
        title="Frontend domain",
        description="Used for rewriting URL's sent in the password reset e-mail by Plone.",
        default="http://localhost:3000",
    )
