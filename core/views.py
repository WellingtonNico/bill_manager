
from django.urls import reverse_lazy
from core.forms import SupportForm
from core.view_classes import CustomContextMixin
from django.views.generic import FormView
from django.contrib.messages.views import SuccessMessageMixin


class SupportView(CustomContextMixin,SuccessMessageMixin,FormView):
    template_name = 'support/support_form.html'
    confirmation_template = 'support/support_sent_confirmation.html'
    form_class = SupportForm
    success_url = reverse_lazy('support_sent_confirmation')
