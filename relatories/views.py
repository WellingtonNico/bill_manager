from django.urls import reverse_lazy
from django.views.generic import TemplateView
from core.view_classes import CustomCreateView,CustomUpdateView
from relatories.models import BillRelatory


class BillRelatoryView(TemplateView):
    template_name = 'relatories/billrelatory_view.html'


class BillRelatoryCreateView(CustomCreateView):
    success_url = reverse_lazy('billrelatory_view')
    model = BillRelatory


class BillRelatoryUpdateView(CustomUpdateView):
    model = BillRelatory

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

