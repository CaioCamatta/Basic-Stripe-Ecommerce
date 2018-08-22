from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create sign up form using UserCreationForm
class SignUpForm(UserCreationForm):
    # OBS: UserCreationForm already has the 'username', 'password1', 'password2' fields so creating them again isn't necessary.
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=255, help_text='eg. youremail@anyemail.com', required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
