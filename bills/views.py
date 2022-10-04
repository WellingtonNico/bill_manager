from django.shortcuts import render
from django.views.generic import ListView,UpdateView,DetailView
from bills.constants import *

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