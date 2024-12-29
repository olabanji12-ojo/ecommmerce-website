from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product


class RegisterCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email...'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter password...'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password...'}),
        }
        help_texts = {
            'username': None,  # Remove help text for username
            'password1': None,  # Remove password1 help text
            'password2': None,  # Remove password2 help text
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = ''
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'