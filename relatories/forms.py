from django.forms import ModelForm, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Layout,Fieldset
from relatories.models import BillRelatory
from datetime import date,datetime


class BillRelatoryForm(ModelForm):
    instance:BillRelatory
    helper = FormHelper()
    helper.layout = Layout(
        Fieldset(
            'Formulário de Relatório',
            'start_year','start_month','end_year','end_month'
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
        model = BillRelatory
        fields = (
            'start_year','start_month','end_year','end_month'
        )

    def __init__(self,*args,**kwargs):
        a = kwargs.pop('custom_kwargs',{})
        self.current_user = a.pop('current_user',None)
        super().__init__(*args,**kwargs)

    def clean(self):
        start_year = self.cleaned_data.get('start_year',None)
        end_year = self.cleaned_data.get('end_year',None)
        start_month = self.cleaned_data.get('start_month',None)
        end_month = self.cleaned_data.get('end_month',None)
        if all((start_year,end_year,start_month,end_month)):
            start_date = date(
                start_year,
                start_month,
                1
            )
            final_date = date(
                end_year,
                end_month,
                1
            )
            today_date = date(
                datetime.now().year,
                datetime.now().month,
                1
            )
            if final_date < start_date:
                raise ValidationError('O período inicial não pode ser mais recente que o período final')
            if final_date > today_date:
                raise ValidationError('O período final não pode ser superior ao mês e ano atuais')

    def clean_start_year(self):
        value = self.cleaned_data['start_year']
        if not len(str(value)) == 4:
            raise ValidationError('O ano deve ter 4 dígitos')
        return value
    
    def clean_end_year(self):
        value = self.cleaned_data['end_year']
        if not len(str(value)) == 4:
            raise ValidationError('O ano deve ter 4 dígitos')
        return value
    
    def is_valid(self) -> bool:
        self.instance.user = self.current_user
        return super().is_valid()

    def save(self,commit=True):
        obj:BillRelatory = super().save(commit=commit)
        obj.enqueue()
        return obj




