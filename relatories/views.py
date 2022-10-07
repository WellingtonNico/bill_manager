from django.urls import reverse_lazy
from django.views.generic import TemplateView
from core.view_classes import CustomCreateView,CustomUpdateView
from relatories.forms import BillRelatoryForm
from relatories.models import BillRelatory


class BillRelatoryView(TemplateView):
    template_name = 'relatories/billrelatory_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rel = self.request.user.has_billrelatory()
        if rel:
            context['form'] = BillRelatoryForm(instance=rel,custom_kwargs={'current_user':self.request.user})
        else:
            context['form'] = BillRelatoryForm(custom_kwargs={'current_user':self.request.user})
        # self.request.user.billrelatory.process()
        return context


class BillRelatoryCreateView(CustomCreateView):
    success_url = reverse_lazy('billrelatory_view')
    model = BillRelatory
    form_class = BillRelatoryForm


class BillRelatoryUpdateView(CustomUpdateView):
    model = BillRelatory
    form_class = BillRelatoryForm
    success_url = reverse_lazy('billrelatory_view')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

