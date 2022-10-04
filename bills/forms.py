from django.forms import ModelForm, ValidationError
from .models import Bill
from bill_categories.models import BillCategory
from bill_chargers.models import BillCharger
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset


class BillModelForm(ModelForm):
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Cadastro de Conta',
            'bill_category','bill_type','installment_total','installment_sequence',
            'bill_charger','created_date','expiration_date',
            'days_to_notify_before_expiration','status','value','note'
        ),
        HTML(
            '''
            <div class="row mt-3 justify-content-center">
                <div class="col text-center">
                    <button type="submit" class="btn btn-success"><i class="material-icons">save</i> salvar</button>
                </div>
                {% if form.instance.id %}
                    <div class="col text-center">
                        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#delete">
                            <i class="material-icons">delete</i> deletar
                        </button>
                    </div>
                {% endif %}
            </div>
            '''
        )
    )

    class Meta:
        model = Bill
        fields = (
            'bill_category','bill_type','installment_total','installment_sequence',
            'bill_charger','created_date','expiration_date',
            'days_to_notify_before_expiration','status','value','note'
        )

    def __init__(self, *args,**kwargs):
        self.current_user = kwargs.pop('current_user')
        super().__init__(*args,**kwargs)

    
    def clean_installment_total(self):
        billType = self.cleaned_data['bill_type']
        installmentTotal = self.cleaned_data['installment_total']
        if billType == 'INSTALLED':
            if not installmentTotal:
                raise ValidationError('Este campo precisa ser preenchido quando o tipo da conta for parcelada')
        return installmentTotal

    def clean_installment_sequence(self):
        billType = self.cleaned_data['bill_type']
        installmentSequence = self.cleaned_data['installment_sequence']
        if billType == 'INSTALLED':
            if not installmentSequence:
                raise ValidationError('Este campo precisa ser preenchido quando o tipo da conta for parcelada')
        return installmentSequence

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid(self)