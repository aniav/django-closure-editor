# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import flatatt
from django.utils.html import escape
from django.utils.safestring import mark_safe

from settings import CLOSURE_MEDIA_URL

CLOSURE_DEFAULT_CONFIG = {
    'buttons': ('BOLD', 'ITALIC', 'UNDERLINE', 'FONT_COLOR', 'BACKGROUND_COLOR',
        'FONT_FACE', 'FONT_SIZE', 'LINK', 'UNDO', 'REDO', 'UNORDERED_LIST',
        'ORDERED_LIST', 'INDENT', 'OUTDENT', 'JUSTIFY_LEFT', 'JUSTIFY_CENTER',
        'JUSTIFY_RIGHT', 'SUBSCRIPT', 'SUPERSCRIPT', 'STRIKE_THROUGH',
        'REMOVE_FORMAT'
     ),
    'plugins': ('BasicTextFormatter', 'RemoveFormatting', 'UndoRedo',
        'ListTabHandler', 'SpacesTabHandler', 'EnterHandler',
        'HeaderFormatter', 'LinkBubble'
    ),
}
class ClosureEditorWidget(forms.Textarea):
    """
    Widget providing Closure Library Editor for Textarea fields
    Set the location of the topmost closure directory in
    CLOSURE_MEDIA_URL
    """
    class Media:
        js = (
            CLOSURE_MEDIA_URL + 'closure/goog/base.js',
            'closure-requirements.js',
        )
        css = {'all': (
            CLOSURE_MEDIA_URL + 'closure/goog/css/common.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/button.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/dialog.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/linkbutton.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/menu.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/menuitem.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/menuseparator.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/tab.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/tabbar.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/toolbar.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/colormenubutton.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/palette.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/colorpalette.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/editor/bubble.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/editor/dialog.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/editor/linkdialog.css',
            CLOSURE_MEDIA_URL + 'closure/goog/css/editortoolbar.css',
        )}

    def __init__(self, content_language=None, attrs=None, 
                 closure_attrs=CLOSURE_DEFAULT_CONFIG):
        super(ClosureEditorWidget, self).__init__(attrs)
        self.closure_attrs = closure_attrs

    def render(self, name, value, attrs={}):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        label_id = self.id_for_label(final_attrs['id'])
        #TODO: make the mess below look at least clean and clear
        html = [u'<div id="%s_toolbar"></div>' % label_id]
        html.append(u'<div id="%s_content"></div>' % label_id)
        html.append(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs), escape(value)))
        html.append('<script type="text/javascript">')
        html.append("""function updateFieldContents() {
            goog.dom.getElement('%s').value = myField.getCleanContents();
        }""" % label_id)
        html.append("var myField = new goog.editor.Field('%s_content');" % label_id)
        for plugin in self.closure_attrs.get('plugins'):
            html.append("myField.registerPlugin(new goog.editor.plugins.%s());" \
                        % plugin)
        html.append('var buttons = [')
        for button in self.closure_attrs.get('buttons'):
            html.append('   goog.editor.Command.%s,' % button)
        html.append('];')
        html.append(u'''
            var myToolbar = goog.ui.editor.DefaultToolbar.makeToolbar(buttons,
                goog.dom.getElement('%s_toolbar'));
            var myToolbarController =
                new goog.ui.editor.ToolbarController(myField, myToolbar);
            goog.events.listen(myField, goog.editor.Field.EventType.DELAYEDCHANGE,
                updateFieldContents);
            myField.makeEditable();
            updateFieldContents();
            </script>
            ''' % (label_id))
        return mark_safe(u'\n'.join(html)) 


