from django.contrib.auth.forms import AuthenticationForm
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
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">login</i> login</button>
                </div>
            </div>
            '''
        )
    )