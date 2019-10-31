.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
kitconcept.voltodemo
==============================================================================

.. image:: https://kitconcept.com/logo.svg
   :alt: kitconcept
   :target: https://kitconcept.com/


.. image:: https://secure.travis-ci.org/collective/kitconcept.voltodemo.png
    :target: http://travis-ci.org/collective/kitconcept.voltodemo

kitconcept.voltodemo is a helper package to setup a Plone site ready to use
with Volto. Drop it in your buildout and then install it. It is used in Volto
itself for testing it.


Usage
-----

https://github.com/plone/volto/blob/master/api/base.cfg#L13

and along with plonesite recipe:

https://github.com/plone/volto/blob/master/api/base.cfg#L13

Demo home page
--------------

It features a hack to make the Plone site Volto Blocks enabled with some demo
content.

Volto Editor
-------------

It enables the Volto Blocks behavior on the ``Document`` content type by
default, enabling Volto editor for that content type.

Disabled content types
----------------------

It disables (fti) of some default content types since they are not ready or
full working yet on Volto side. So, ``Collections``, ``Link`` and ``Events``
are disabled.

CORS profile
------------

A quick helper for enable CORS for development config is also provided in the
``kitconcept.voltodemo`` module. So you can call::

  <include package="kitconcept.voltodemo.cors" />

from you ZCML while developing.

Versions compatibility
----------------------

kitconcept.voltodemo < 2 Volto 3 and Volto 4 until alpha 9
kitconcept.voltodemo >= 2 Volto 4 (from alpha 10)
