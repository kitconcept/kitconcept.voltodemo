# -*- coding: utf-8 -*-
from .interfaces import IHomepage
from plone.dexterity.content import Container
from zope.interface import implements


class Homepage(Container):
    implements(IHomepage)
