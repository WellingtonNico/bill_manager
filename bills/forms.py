from datetime import datetime
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
            'days_to_notify_before_expiration','status','value','note','payment_date',
            'payment_type'
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
            'days_to_notify_before_expiration','status','value','note','payment_date',
            'payment_type'
        )

    def __init__(self, *args,**kwargs):
        custom_kwargs = kwargs.pop('custom_kwargs')
        self.current_user = custom_kwargs['current_user']
        super().__init__(*args,**kwargs)
        self.fields['bill_category'].queryset = self.current_user.get_billcategories()
        self.fields['bill_charger'].queryset = self.current_user.get_billchargers()
    
    def clean_installment_total(self):
        billType = self.cleaned_data['bill_type']
        installmentTotal = self.cleaned_data['installment_total']
        if billType == 'INSTALLED':
            if not installmentTotal:
                raise ValidationError('Este campo precisa ser preenchido quando a conta for parcelada')
        return installmentTotal

    def clean_installment_sequence(self):
        billType = self.cleaned_data['bill_type']
        installmentSequence = self.cleaned_data['installment_sequence']
        if billType == 'INSTALLED':
            if not installmentSequence:
                raise ValidationError('Este campo precisa ser preenchido quando a conta for parcelada')
        return installmentSequence

    def clean_expiration_date(self):
        created_date = self.cleaned_data['created_date']
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date:
            if created_date > expiration_date:
                raise ValidationError('A data de vencimento não pode ser inferior a data de criação')
        return expiration_date

    def clean_payment_date(self):
        status = self.cleaned_data['status']
        payment_date = self.cleaned_data['payment_date']
        if payment_date:
            if payment_date > datetime.now().date():
                raise ValidationError('A data de pagamento não pode ser superior ao dia atual')
        elif status == 'PAID':
            raise ValidationError('Ao alterar o status para PAGA, deve informar a data do pagamento')
        return payment_date

    def clean_payment_type(self):
        status = self.cleaned_data['status']
        payment_type = self.cleaned_data['payment_type']
        if status == 'PAID' and not payment_type:
            raise ValidationError('Ao alterar o status para PAGA, é necessário informar o tipo do pagamento')
        return payment_type

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid()