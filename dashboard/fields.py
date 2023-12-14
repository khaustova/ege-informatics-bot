from django.db import models
from .forms import MDEditorFormField


class MDEditorField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': MDEditorFormField,
        }
        defaults.update(kwargs)
        return super(MDEditorField, self).formfield(**defaults)