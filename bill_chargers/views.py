from bill_chargers.forms import BillChargerModelForm
from bill_chargers.models import BillCharger
from core.view_classes import CustomCreateView, CustomListView, CustomUpdateView
from django.urls import reverse_lazy


class BillChargerListView(CustomListView):
    get_queryset_function_to_eval = 'self.request.user.get_billchargers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill_charger_create_form'] = BillChargerModelForm(custom_kwargs={'current_user':self.request.user})
        return context


class BillChargerCreateView(CustomCreateView):
    model = BillCharger
    form_class = BillChargerModelForm
    success_url = reverse_lazy('billcharger_list')


class BillChargerUpdateView(CustomUpdateView):
    form_class = BillChargerModelForm

    def get_queryset(self):
        return self.request.user.get_billchargers()
    
