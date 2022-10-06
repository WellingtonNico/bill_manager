from datetime import datetime
from django.forms import BooleanField, ModelForm, ValidationError, FileField, CheckboxInput
from django.conf import settings
from .models import Bill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset


class BillModelForm(ModelForm):
    create_all_installments = BooleanField(
        label='Cadastrar parcelas subsequentes',required=False,
        widget=CheckboxInput(attrs={'class':'check-form-input'}),
        help_text='Ao habilitar, serão cadastradas as demais parcelas, começando do número de parcela deste cadastro - válido somente ao criar cadastro'
    )
    instance:Bill
    helper = FormHelper()
    

    class Meta:
        model = Bill
        fields = (
            'bill_category','bill_type','installment_total','installment_sequence',
            'bill_charger','created_date','expiration_date',
            'days_to_notify_before_expiration','status','value'
        )

    def __init__(self, *args,**kwargs):
        custom_kwargs = kwargs.pop('custom_kwargs')
        self.current_user = custom_kwargs['current_user']
        super().__init__(*args,**kwargs)
        self.fields['bill_category'].queryset = self.current_user.get_billcategories()
        self.fields['bill_charger'].queryset = self.current_user.get_billchargers()
        self.helper.layout =Layout(
            Fieldset(
                'Conta',
                'status','bill_category','bill_charger','bill_type','installment_total',
                'installment_sequence','value','note'
            ) if self.instance.id else 
            Fieldset(
                'Conta',
                'status','bill_category','bill_charger','bill_type','installment_total',
                'installment_sequence','create_all_installments','value','note'
            ),
            HTML('<hr>'),
            Fieldset(
                'Datas',
                'created_date','expiration_date','days_to_notify_before_expiration',
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

    def clean_create_all_installments(self):
        create_all_installments = self.cleaned_data.get('create_all_installments',None)
        if create_all_installments == True:
            self.instance.create_all_installments = True

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
        bill_type = self.cleaned_data['bill_type']
        if expiration_date:
            if created_date > expiration_date:
                raise ValidationError('A data de vencimento não pode ser inferior a data de criação')
        if bill_type == 'INSTALLED' and not expiration_date:
            raise ValidationError('A data de vencimento é obrigatória quando o tipo da conta for PARCELADA')
        return expiration_date

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid()


class BillPaymentForm(ModelForm):
    class Meta:
        model = Bill
        fields = (
            'payment_date','payment_type','bank','payment_proof_file'
        )

    helper = FormHelper()
    helper.layout =Layout(
        Fieldset(
            'Formulário de pagamento',
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
                    <button type="submit" class="btn btn-success"><i class="material-icons">done</i> pagar</button>
                </div>
            </div>
            '''
        )
    )

    def __init__(self, *args, **kwargs):
        kwargs.pop('custom_kwargs',None)
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].required = True
        self.fields['payment_type'].required = True
        self.fields['bank'].required = True

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
