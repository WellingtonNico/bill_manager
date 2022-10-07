from django.views.generic import ListView, CreateView, UpdateView
from bill_categories.forms import BillCategoryModelForm
from core.view_classes import CustomCreateView, CustomListView, CustomUpdateView
from .models import BillCategory
from django.urls import reverse_lazy


class BillCategoryListView(CustomListView):
    extra_context = {
        'PAGE_SIZES':[5,10,20,30,40,50]
    }
    get_queryset_function_to_eval = 'self.request.user.get_billcategories'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill_category_create_form'] = BillCategoryModelForm(custom_kwargs={'current_user':self.request.user})
        return context


class BillCategoryCreateView(CustomCreateView):
    model = BillCategory
    form_class = BillCategoryModelForm
    success_url = reverse_lazy('billcategory_list')


class BillCategoryUpdateView(CustomUpdateView):
    form_class = BillCategoryModelForm

    def get_queryset(self):
        return self.request.user.get_billcategories()
    




