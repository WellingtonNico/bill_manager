from django.forms import ModelForm, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML
from relatories.models import BillRelatory
from datetime import date,datetime


class BillRelatoryForm(ModelForm):
    instance:BillRelatory
    helper = FormHelper()

    class Meta:
        model = BillRelatory
        fields = (
            'start_year','start_month','end_year','end_month'
        )

    def clean(self):
        start_year = self.cleaned_data.get('start_year',None)
        final_year = self.cleaned_data.get('final_year',None)
        start_month = self.cleaned_data.get('start_month',None)
        final_month = self.cleaned_data.get('final_month',None)
        if all((start_year,final_year,start_month,final_month)):
            start_date = date(
                start_year,
                start_month,
                1
            )
            final_date = date(
                final_year,
                final_month,
                1
            )
            today_date = date(
                datetime.now().year,
                datetime.now().month,
                1
            )
            if final_date < start_date:
                raise ValidationError({'start_month':'O período inicial não pode ser mais recente que o período final'})
            if final_date > today_date:
                raise ValidationError({'final_month':'O período final não pode ser superior ao mês e ano atuais'})

    def clean_start_year(self):
        value = self.cleaned_data['start_year']
        if not len(str(value)) == 4:
            raise ValidationError('O ano deve ter no mínimo 4 dígitos')
        return value
    
    def clean_final_year(self):
        value = self.cleaned_data['final_year']
        if not len(str(value)) == 4:
            raise ValidationError('O ano deve ter no mínimo 4 dígitos')
        return value

    def save(self,commit=True):
        obj:BillRelatory = super().save(commit=commit)
        obj.enqueue()
        return obj




