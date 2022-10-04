from django.shortcuts import render
from django.views.generic import ListView,UpdateView,DetailView
from bills.constants import *

from core.view_classes import ListViewFilterMixin


class BillListView(ListViewFilterMixin,ListView):

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size',30)

    def get_queryset(self):
        return self.request.user.get_bills().filter(**self.build_filters_dict())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['BILL_TYPES'] = BILL_TYPES
        context['BILL_STATUSES'] = BILL_STATUSES
        context['PAGE_SIZES'] = [5,10,20,30,40,50]
        return context