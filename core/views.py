
from django.urls import reverse_lazy
from core.forms import AccessSolicitationForm, SupportForm
from core.view_classes import CustomContextMixin
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin


class SupportView(CustomContextMixin,SuccessMessageMixin,FormView):
    template_name = 'support/support_form.html'
    form_class = SupportForm
    success_url = reverse_lazy('support_sent_confirmation')


class AccessSolicitationView(SuccessMessageMixin,FormView):
    template_name = 'support/contact_form.html'
    form_class = AccessSolicitationForm
    success_url = reverse_lazy('login')

    def get_success_message(self, cleaned_data) -> str:
        return 'Recebemos a sua solicitação, assim que possível entraremos em contato. Obrigado!'
    
