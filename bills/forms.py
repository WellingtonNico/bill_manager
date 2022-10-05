from datetime import datetime
from django.forms import ModelForm, ValidationError, FileField, FileInput
from django.conf import settings

from bills.constants import PAYMENT_PROOF_PREFIX_NAME
from .models import Bill
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset


class BillModelForm(ModelForm):
    instance:Bill
    payment_proof = FileField(
        label='Comprovante de pagamento',max_length=settings.PAYMENT_PROOFS_MAX_LENGTH_KB*1024,required=False,
        help_text=f'Caso o status for PAGO pode estar anexando um comprovante, caso já exista um comprovante, o mesmo será sobrescrito. Tamamho máximo {settings.PAYMENT_PROOFS_MAX_LENGTH_KB} KB', 
    )
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
            'payment_date','payment_type','payment_proof'
        ),
        HTML(
            '''
            {% if form.instance.id %}
                {% if form.instance.get_payment_proof_fulldir %}
                    <a download href="{% url 'bill_downoad_payment_proof' form.instance.id %}">Baixar comprovante</a>
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
        if billType == 'INSTALLED':
            installmentTotal = self.cleaned_data['installment_total']
            if not installmentTotal:
                raise ValidationError('Este campo precisa ser preenchido quando a conta for parcelada')
            return installmentTotal
        else:
            return None

    def clean_installment_sequence(self):
        billType = self.cleaned_data['bill_type']
        if billType == 'INSTALLED':
            installmentSequence = self.cleaned_data['installment_sequence']
            installmentTotal = self.cleaned_data['installment_total']
            if not installmentSequence:
                raise ValidationError('Este campo precisa ser preenchido quando a conta for parcelada')
            if installmentSequence > installmentTotal:
                raise ValidationError('O número da parcela não pode ser superior ao número total de parcelas')
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
    
    def clean_payment_proof(self):
        status = self.cleaned_data['status']
        self.payment_proof_file = self.cleaned_data['payment_proof']
        if status == 'PAID' and self.payment_proof_file:
            if self.instance.id:
                if len(self.payment_proof_file) > settings.PAYMENT_PROOFS_MAX_LENGTH_KB*1024:
                    raise ValidationError(f'O comprovante de pagamento excede o tamanho máximo permitido de {settings.PAYMENT_PROOFS_MAX_LENGTH_KB} KB')
                if not 'image' in self.payment_proof_file.content_type and not 'pdf' in self.payment_proof_file.content_type:
                    raise ValidationError('Formato de arquivo não aceito, são permitidos somente PDFs e imagens')
                
                self.instance.payment_proof_file_name = self.payment_proof_file.name
            else:
                raise ValidationError('Para pode adicionar um comprovante, primeiro é necessário salvar o cadastro')
        return None

    def is_valid(self):
        self.instance.user = self.current_user
        return super().is_valid()

    def save(self, commit=True):
        if hasattr(self,'payment_proof_file') and commit:
            self.instance.delete_payment_proof()
            open(
                f"{self.current_user.get_payment_proofs_dir()}{PAYMENT_PROOF_PREFIX_NAME}{self.instance.id}.{self.payment_proof_file.name.split('.')[-1]}",
                '+wb'
            ).write(self.payment_proof_file.read())
        return super().save(commit)