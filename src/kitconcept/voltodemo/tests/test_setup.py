# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from kitconcept.voltodemo.testing import KITCONCEPTVOLTODEMO_CORE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that kitconcept.voltodemo is properly installed."""

    layer = KITCONCEPTVOLTODEMO_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if kitconcept.voltodemo is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'kitconcept.voltodemo'))

    def test_browserlayer(self):
        """Test that IKitconceptvoltodemoCoreLayer is registered."""
        from kitconcept.voltodemo.interfaces import (
            IKitconceptvoltodemoCoreLayer)
        from plone.browserlayer import utils
        self.assertIn(IKitconceptvoltodemoCoreLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = KITCONCEPTVOLTODEMO_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['kitconcept.voltodemo'])

    def test_product_uninstalled(self):
        """Test if kitconcept.voltodemo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'kitconcept.voltodemo'))

    def test_browserlayer_removed(self):
        """Test that IKitconceptvoltodemoCoreLayer is removed."""
        from kitconcept.voltodemo.interfaces import IKitconceptvoltodemoCoreLayer
        from plone.browserlayer import utils
        self.assertNotIn(IKitconceptvoltodemoCoreLayer, utils.registered_layers())
