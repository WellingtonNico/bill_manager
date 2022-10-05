from django.views.generic import ListView, CreateView, UpdateView
from bill_categories.forms import BillCategoryModelForm
from core.view_classes import CustomCreateView, CustomListView, CustomUpdateView
from .models import BillCategory


class BillCategoryListView(CustomListView):
    extra_context = {
        'PAGE_SIZES':[5,10,20,30,40,50]
    }
    get_queryset_function_to_eval = 'self.request.user.get_billcategories'


class BillCategoryCreateView(CustomCreateView):
    model = BillCategory
    form_class = BillCategoryModelForm


class BillCategoryUpdateView(CustomUpdateView):
    form_class = BillCategoryModelForm

    def get_queryset(self):
        return self.request.user.get_billcategories()
    




