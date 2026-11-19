from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "excerpt", "content", "category", "tags", "status")
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "content": forms.Textarea(attrs={"rows": 12}),
            "tags": forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a thoughtful comment..."})}
