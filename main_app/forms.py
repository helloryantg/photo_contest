from django.forms import ModelForm, Form, CharField, PasswordInput
from .models import Comment

class LoginForm(Form):
    username = CharField(label="Username", max_length=64)
    password = CharField(widget=PasswordInput())

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
