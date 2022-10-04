from django.urls import reverse_lazy
from django.views.generic import ListView,UpdateView,DetailView,DeleteView,CreateView
from bills.constants import *
from bills.forms import BillModelForm
from bills.models import Bill

from core.view_classes import ListViewFilterMixin


class BillListView(ListViewFilterMixin,ListView):

    default_ordering = '-created_date'

    def get_queryset(self):
        querySet = self.request.user.get_bills().filter(**self.build_filters_dict())
        ordering = self.get_ordering()
        if ordering:
            return querySet.order_by(ordering)
        return querySet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['BILL_TYPES'] = BILL_TYPES
        context['BILL_STATUSES'] = BILL_STATUSES
        context['BILL_ORDERING_OPTIONS'] = BILL_ORDERING_OPTIONS
        context['PAGE_SIZES'] = [5,10,20,30,40,50]
        return context


class BillCreateView(CreateView):
    model = Bill
    form_class = BillModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class BillUpdateView(UpdateView):
    form_class = BillModelForm
    
    def get_queryset(self):
        return self.request.user.get_bills()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class BillDeleteView(DeleteView):
    success_url = reverse_lazy('bill_list')

    def get_queryset(self):
        return self.request.user.get_bills()