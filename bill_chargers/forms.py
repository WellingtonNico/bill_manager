from django.forms import ModelForm
from .models import BillCharger
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset


class BillChargerModelForm(ModelForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Cadastro de Cobrador',
            'name','phone','email'
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">save</i> salvar</button>
                </div>
            </div>
            '''
        )
    )

    class Meta:
        model = BillCharger
        fields = (
            'name','phone','email'
        )

    def __init__(self, *args,**kwargs):
        self.current_user = kwargs.pop('current_user')
        super().__init__(*args,**kwargs)

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid()