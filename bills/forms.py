from datetime import datetime
from django.forms import ModelForm, ValidationError, FileField
from django.conf import settings
from .models import Bill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset


class BillModelForm(ModelForm):
    instance:Bill
    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Conta',
            'status','bill_category','bill_charger','bill_type','installment_total',
            'installment_sequence','value','note'
        ),
        HTML('<hr>'),
        Fieldset(
            'Datas',
            'created_date','expiration_date','days_to_notify_before_expiration',
        ),
        HTML('<hr>'),
        Fieldset(
            'Pagamento',
            'payment_date','payment_type','bank','payment_proof_file'
        ),
        HTML(
            '''
            {% if form.instance.id and not form.payment_proof_file.errors %}
                {% if form.instance.payment_proof_file.file is not none %}
                    <a download href="{% url 'bill_payment_proof_download' form.instance.id %}">Baixar comprovante</a>
                {% endif %}
            {% endif %}
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
            'payment_type','bank','payment_proof_file'
        )

    def __init__(self, *args,**kwargs):
        custom_kwargs = kwargs.pop('custom_kwargs')
        self.current_user = custom_kwargs['current_user']
        super().__init__(*args,**kwargs)
        self.fields['bill_category'].queryset = self.current_user.get_billcategories()
        self.fields['bill_charger'].queryset = self.current_user.get_billchargers()
    
    def clean_installment_total(self):
        billType = self.cleaned_data['bill_type']
        if billType == 'INSTALLED':
            installmentTotal = self.cleaned_data['installment_total']
            if not installmentTotal:
                raise ValidationError('Este campo precisa ser preenchido quando a conta for parcelada')
            if installmentTotal <=1:
                raise ValidationError('Não use o tipo de conta PARCELADA com somente uma ou nenhuma parcela')
            return installmentTotal
        else:
            return None

    def clean_installment_sequence(self):
        billType = self.cleaned_data['bill_type']
        if billType == 'INSTALLED':
            installmentSequence = self.cleaned_data['installment_sequence']
            installmentTotal = self.cleaned_data.get('installment_total',None)
            if not installmentSequence:
                raise ValidationError('Este campo precisa ser preenchido quando a conta for parcelada')
            if installmentTotal != None:
                if installmentSequence > installmentTotal:
                    raise ValidationError('O número da parcela não pode ser superior ao número total de parcelas')
            else:
                raise ValidationError('Não foi possível validar este campo pois o campo de total de parcelas possui erro')
            return installmentSequence
        else:
            return None

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
        if status != 'PAID':
            return None
        elif not payment_date:
            raise ValidationError('Ao alterar o status para PAGA, deve informar a data do pagamento')
        elif payment_date > datetime.now().date():
            raise ValidationError('A data de pagamento não pode ser superior ao dia atual')
        return payment_date

    def clean_payment_type(self):
        status = self.cleaned_data['status']
        payment_type = self.cleaned_data['payment_type']
        if status != 'PAID':
            return None
        elif not payment_type:
            raise ValidationError('Ao alterar o status para PAGA, é necessário informar o tipo do pagamento')
        return payment_type

    def clean_bank(self):
        status = self.cleaned_data['status']
        bank = self.cleaned_data['bank']
        if status != 'PAID':
            return None
        elif not bank:
            raise ValidationError('Ao alterar o status para PAGA, é necessário informar o banco')
        return bank
    
    def clean_payment_proof_file(self):
        status = self.cleaned_data['status']
        payment_proof_file = self.cleaned_data['payment_proof_file']
        if status == 'PAID':
            return payment_proof_file
        elif payment_proof_file:
            raise ValidationError('Só é possível adicionar um comprovante quando o status por PAGO')
        return False

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid()
