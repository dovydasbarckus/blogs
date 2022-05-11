from tinymce.models import HTMLField
from .models import ArticleComment
from django import forms


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = fields = '__all__'
        widgets = {
            'article': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
            'created': forms.HiddenInput(),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }
