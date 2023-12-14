from django import forms
from .widgets import MDEditorWidget

   
class MDEditorFormField(forms.fields.CharField):
    def __init__(self, config_name='default', *args, **kwargs):
        kwargs.update({
            'widget': MDEditorWidget()
        })
        super(MDEditorFormField, self).__init__(*args, **kwargs)   