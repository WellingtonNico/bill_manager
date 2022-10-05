from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
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