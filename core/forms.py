from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm,PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset


class CustomAuthenticationForm(AuthenticationForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Login',
            'username','password'
        ),
        HTML(
            '''
            {% if form.errors %}
                <a href="{% url 'password_reset' %}" class="my-1">Esqueci minha senha</a>
            {% endif %}
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">login</i> login</button>
                </div>
            </div>
            '''
        )
    )

class CustomPasswordResetForm(PasswordResetForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Recuperação de senha',
            'email',
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> enviar email</button>
                </div>
            </div>
            '''
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Recuperação de senha',
            'new_password1','new_password2'
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> alterar</button>
                </div>
            </div>
            '''
        )
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Alteração de senha de senha',
            'old_password','new_password1','new_password2'
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> alterar</button>
                </div>
            </div>
            '''
        )
    )