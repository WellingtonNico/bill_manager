from django.views.generic import ListView, CreateView, UpdateView
from bill_categories.forms import BillCategoryModelForm
from core.view_classes import ListViewFilterMixin
from .models import BillCategory


class BillCategoryListView(ListViewFilterMixin,ListView):

    def get_queryset(self):
        return self.request.user.get_billcategories().filter(**self.build_filters_dict())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PAGE_SIZES'] = [5,10,20,30,40,50]
        return context


class BillCategoryCreateView(CreateView):
    model = BillCategory
    form_class = BillCategoryModelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


class BillCategoryUpdateView(UpdateView):
    form_class = BillCategoryModelForm

    def get_queryset(self):
        return self.request.user.get_billcategories()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs





