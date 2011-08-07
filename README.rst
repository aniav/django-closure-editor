Django Closure Editor
================
**Django Closure Library Editor integration.**

Provides a ``ClosureEditorWidget`` for textarea fields

.. contents:: Contents
    :depth: 3

Installation
------------

#. Install or add django-closure-editor to your python path.

#. Add ``closure_editor`` to your INSTALLED_APPS setting.

#. Copy the ``media`` directory contents into any directory within your media root. You can override the location in your settings (see below).

#. Add a CLOSURE_MEDIA_URL setting to the project's ``settings.py`` file. This setting specifies a URL prefix to the closure JS and CSS media. Make sure to use a trailing slash::

    CLOSURE_MEDIA_URL = '/media/closure-library/'

Usage
-----

Use the included ``ClosureEditorWidget`` as the widget for a formfield. For example::

    from django import forms
    from closure_editor.widgets import ClosureEditorWidget

    class TextForm(forms.Form):
        closure_field = forms.CharField(widget=ClosureEditorWidget())

**NOTE**: If you're using custom views remember to include the provided JS and CSS files in your form's media either through ``{{ form.media }}`` or through a ``<script>`` tag. Admin will do this for you automatically. See `Django's Form Media docs <http://docs.djangoproject.com/en/dev/topics/forms/media/>`_ for more info.
