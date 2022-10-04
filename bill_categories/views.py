from django.views.generic import ListView
from core.view_classes import ListViewFilterMixin
from .models import BillCategory


class BillCategoryListView(ListViewFilterMixin,ListView):

    def get_queryset(self):
        return self.request.user.get_billcategories().filter(**self.build_filters_dict())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PAGE_SIZES'] = [5,10,20,30,40,50]
        return context
