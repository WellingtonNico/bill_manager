from datetime import datetime
from django.forms import BooleanField, FileInput, ModelForm, ValidationError, CheckboxInput, CharField, TextInput
from .models import Bill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset,Div

class BillModelForm(ModelForm):
    value = CharField(min_length=0,max_length=255,label='Valor')
    instance:Bill
    helper = FormHelper()
    
    class Meta:
        model = Bill
        fields = (
            'bill_category','bill_type','installment_total',
            'bill_charger','expiration_date',
            'value'
        )

    def __init__(self, *args,**kwargs):
        custom_kwargs = kwargs.pop('custom_kwargs')
        self.current_user = custom_kwargs['current_user']
        super().__init__(*args,**kwargs)
        self.fields['bill_category'].queryset = self.current_user.get_billcategories()
        self.fields['bill_charger'].queryset = self.current_user.get_billchargers()
        self.helper.layout =Layout(
            Div('bill_category','bill_charger',css_class='col-12 col-md-4'),
            Div('bill_type','expiration_date',css_class='col-12 col-md-4'),
            Div('installment_total','value',css_class='col-12 col-md-4'),
            HTML(
                '''
                {% if form.instance.id and not form.payment_proof_file.errors %}
                    {% if form.instance.payment_proof_file.file is not none %}
                        <a download href="{% url 'bill_payment_proof_download' form.instance.id %}">Baixar Comprovante</a>
                    {% endif %}
                {% endif %}
                <div class="row mt-3 justify-content-center">
                    <div class="col text-center">
                        <button type="submit" class="btn btn-success"><i class="material-icons">save</i> Salvar</button>
                    </div>
                    {% if form.instance.id %}
                        <div class="col text-center">
                            <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#delete">
                                <i class="material-icons">delete</i> Deletar
                            </button>
                        </div>
                    {% endif %}
                </div>
                '''
            )
        )
    def clean_value(self):
        return  float(self.cleaned_data['value'].replace('.','').replace(',','.'))
    
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

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        bill_type = self.cleaned_data['bill_type']
        if bill_type == 'INSTALLED' and not expiration_date:
            raise ValidationError('A data de vencimento é obrigatória quando o tipo da conta for PARCELADA')
        return expiration_date

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid()


class BillUndoPaymentForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('payment_date','payment_type','bank')

    def save(self, commit: bool = ...):
        self.instance.payment_proof_file = None
        self.instance.status = 'UNDEFINED'
        return super().save(commit)


class BillPaymentForm(ModelForm):
    class Meta:
        model = Bill
        fields = (
            'payment_date','payment_type','bank','payment_proof_file'
        )

    helper = FormHelper()
    helper.layout =Layout(
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
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> Pagar</button>
                </div>
            </div>
            '''
        )
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop('custom_kwargs',None)
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].required = True
        self.fields['payment_date'].initial = datetime.now().date()
        self.fields['payment_type'].required = True
        self.fields['bank'].required = True
        self.fields['payment_proof_file'].widget.attrs = {
            'accept':'application/pdf,image/*'
        }

    def clean_payment_date(self):
        payment_date = self.cleaned_data['payment_date']
        if not payment_date:
            raise ValidationError('Ao alterar o status para PAGA, deve informar a data do pagamento')
        elif payment_date > datetime.now().date():
            raise ValidationError('A data de pagamento não pode ser superior ao dia atual')
        return payment_date

    def is_valid(self) -> bool:
        
        self.instance.status = 'PAID'
        return super().is_valid()
