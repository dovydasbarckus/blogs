from django.contrib.auth.models import User
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


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
