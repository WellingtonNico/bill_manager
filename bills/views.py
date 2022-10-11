from core.view_classes import CustomCreateView, CustomUpdateView, CustomListView
from bills.constants import *
from bills.models import Bill
from bills.forms import BillModelForm, BillPaymentForm, BillUndoPaymentForm
from django.http import FileResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView,DetailView,UpdateView


class BillListView(CustomListView):
    default_ordering = '-created_date' 
    get_queryset_function_to_eval = 'self.request.user.get_bills'
    default_page_size = 13

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill_create_form'] = BillModelForm(custom_kwargs={'current_user':self.request.user})
        context['BILL_TYPES']=BILL_TYPES
        context['BILL_STATUSES']=BILL_STATUSES
        context['BILL_ORDERING_OPTIONS']=BILL_ORDERING_OPTIONS
        context['BILL_PAYMENT_TYPES']=BILL_PAYMENT_TYPES
        context['BILL_PAYMENT_BANKS']=BILL_PAYMENT_BANKS
        context['PAYMENT_FORM']=BillPaymentForm()
        return context


class BillCreateView(CustomCreateView):
    model = Bill
    form_class = BillModelForm


class BillUpdateView(CustomUpdateView):
    form_class = BillModelForm
    
    def get_queryset(self):
        return self.request.user.get_bills()


class BillDeleteView(DeleteView):
    success_url = reverse_lazy('bill_list')

    def get_queryset(self):
        return self.request.user.get_bills()


class BillPaymentProofDownloadView(DetailView):
    def get_queryset(self):
        return self.request.user.get_bills()

    def get(self,request,*args,**kwargs):
        obj:Bill = self.get_object()
        fileResponse = FileResponse(
            obj.payment_proof_file.file
        )
        return fileResponse


class BillUndoPaymentUpdateView(SuccessMessageMixin,UpdateView):
    success_message = 'Estorno realizado com sucesso!'
    form_class = BillUndoPaymentForm
    success_url = reverse_lazy('bill_list')

    def get_queryset(self):
        return self.request.user.get_bills()


class BillPaymentUpdateView(CustomUpdateView):
    success_url = reverse_lazy('bill_list')
    template_name_suffix = '_payment_form'
    form_class = BillPaymentForm

    def get_queryset(self):
        return self.request.user.get_bills()
    
    def get_success_message(self,cleaned_data):
        return 'Pagamento efetuado com sucesso!'

