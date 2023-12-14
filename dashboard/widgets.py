from django import forms


class MDEditorWidget(forms.Textarea):
    template_name = 'dashboard/md_editor.html'

    def _get_media(self):
        return forms.Media(
            css={
                "all": ("dashboard/css/md_editor.css",)
            },
            js=(
                "dashboard/js/md_editor.js",
            ))
    media = property(_get_media)