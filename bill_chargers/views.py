from django.views.generic import ListView, CreateView, UpdateView
from bill_chargers.forms import BillChargerModelForm
from bill_chargers.models import BillCharger
from core.view_classes import ListViewFilterMixin


class BillChargerListView(ListViewFilterMixin,ListView):

    def get_queryset(self):
        return self.request.user.get_billchargers().filter(**self.build_filters_dict())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PAGE_SIZES'] = [5,10,20,30,40,50]
        return context


class BillChargerCreateView(CreateView):
    model = BillCharger
    form_class = BillChargerModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class BillChargerUpdateView(UpdateView):
    form_class = BillChargerModelForm

    def get_queryset(self):
        return self.request.user.get_billchargers()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs