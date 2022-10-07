from bill_chargers.forms import BillChargerModelForm
from bill_chargers.models import BillCharger
from core.view_classes import CustomCreateView, CustomListView, CustomUpdateView
from django.urls import reverse_lazy


class BillChargerListView(CustomListView):

    def get_queryset(self):
        return self.request.user.get_billchargers().filter(**self.build_filters_dict())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill_charger_create_form'] = BillChargerModelForm(custom_kwargs={'current_user':self.request.user})
        context['PAGE_SIZES']=[5,10,20,30,40,50]
        return context


class BillChargerCreateView(CustomCreateView):
    model = BillCharger
    form_class = BillChargerModelForm
    success_url = reverse_lazy('billcharger_list')


class BillChargerUpdateView(CustomUpdateView):
    form_class = BillChargerModelForm

    def get_queryset(self):
        return self.request.user.get_billchargers()
    
