from core.view_classes import CustomCreateView, CustomUpdateView, CustomListView
from bills.constants import *
from bills.models import Bill
from bills.forms import BillModelForm, BillPaymentForm
from django.http import FileResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DeleteView,DetailView


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


class BillUndoPaymentUpdateView(CustomUpdateView):

    def get_queryset(self):
        return self.request.user.get_bills()

    def post(self,request,*args,**kwargs):
        obj:Bill = self.get_object()
        obj.payment_date = None
        obj.payment_type = None
        obj.bank = None
        obj.payment_proof_file = None
        obj.status = 'UNDEFINED'
        obj.save()
        return redirect(reverse_lazy('bill_list'))

    def get_sucess_message(self,cleaned_data):
        return 'Estorno realizado com sucesso!'


class BillPaymentUpdateView(CustomUpdateView):
    success_url = reverse_lazy('bill_list')
    template_name_suffix = '_payment_form'
    form_class = BillPaymentForm

    def get_queryset(self):
        return self.request.user.get_bills()
    
    def get_success_message(self,cleaned_data):
        return 'Pagamento efetuado com sucesso!'

