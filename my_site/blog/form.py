from django import forms
from .models import Post
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('post', 'created_at',)
        # widgets = {
        #     'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
        #     'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Comment'}),
        # }
        labels = {
            'author_name': 'Name',
            'email': 'Email (optional)',
            'text': 'Comment',
        }