from django.forms import forms
from core.forms import *
from .models import User

class UserFormMixin:
    def clean_first_name(self):
        value = self.cleaned_data['first_name']
        if not value:
            raise forms.ValidationError('Este campo não pode ficar em branco')
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name']
        if not value:
            raise forms.ValidationError('Este campo não pode ficar em branco')
        return value

    def clean_email_name(self):
        value = self.cleaned_data['email']
        if not value:
            raise forms.ValidationError('Este campo não pode ficar em branco')
        return value
