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

class UserCreateModelForm(UserFormMixin,CustomModelForm):
    password1 = forms.CharField(label='Senha',
        widget=forms.PasswordInput,required=True)
    password2 = forms.CharField(label='Confirmação de senha',
        widget=forms.PasswordInput,required=True,
        help_text="Digite a mesma senha do campo acima.")
    custom_field_attributes = (
        (
            FORM_CONTROL_EMAIL,
            ('email',)
        ),
        (
            DEFAULT_FORM_CONTROL,
            ('first_name','last_name',)
        ),
        (
            DEFAULT_CHECK_BOX,
            ('is_domain_admin','is_for_external_access','is_active')
        ),
        (
            FORM_CONTROL_PASSWORD,
            ('password1','password2',)
        ),
    )
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'document'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not all((password1,password2)):
            raise forms.ValidationError('É necessário informar as senhas')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('As senhas digitadas não são combinam')
        self.instance.set_password(password1)
        return password2

    def is_valid(self)->bool:
        self.instance.is_superuser = False
        return super().is_valid()