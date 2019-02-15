# -*- coding: utf-8 -*-
from kitconcept.voltodemo.interfaces import IKitconceptvoltodemoCoreLayer
from plone.restapi.batching import HypermediaBatch
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.expansion import expandable_elements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer

import json


@implementer(ISerializeToJson)
@adapter(IPloneSiteRoot, IKitconceptvoltodemoCoreLayer)
class SerializeSiteRootToJson(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _build_query(self):
        path = '/'.join(self.context.getPhysicalPath())
        query = {'path': {'depth': 1, 'query': path},
                 'sort_on': 'getObjPositionInParent'}
        return query

    def __call__(self, version=None):
        version = 'current' if version is None else version
        if version != 'current':
            return {}

        query = self._build_query()

        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(query)

        batch = HypermediaBatch(self.request, brains)

        result = {
            # '@context': 'http://www.w3.org/ns/hydra/context.jsonld',
            '@id': batch.canonical_url,
            'id': self.context.id,
            '@type': 'Plone Site',
            'title': self.context.Title(),
            'description': self.context.description,
            'parent': {},
            'is_folderish': True,
            'tiles': json.loads(getattr(self.context, 'tiles', '{}')),
            'tiles_layout': json.loads(getattr(self.context, 'tiles_layout', '{}')) # noqa
        }

        # Insert expandable elements
        result.update(expandable_elements(self.context, self.request))

        result['items_total'] = batch.items_total
        if batch.links:
            result['batching'] = batch.links

        result['items'] = [
            getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
            for brain in batch
        ]

        return result
