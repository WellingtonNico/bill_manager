from django.shortcuts import render
from django.views.generic import ListView,UpdateView,DetailView
from bills.constants import *

from core.view_classes import ListViewFilterMixin


class BillListView(ListViewFilterMixin,ListView):
    paginate_by = 3

    def get_queryset(self):
        return self.request.user.get_bills().filter(**self.build_filters_dict())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['BILL_TYPES'] = BILL_TYPES
        context['BILL_STATUSES'] = BILL_STATUSES
        return context