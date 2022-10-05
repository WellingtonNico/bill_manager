from io import BytesIO
from django.urls import reverse_lazy
from django.views.generic import DeleteView,DetailView
from bills.constants import *
from bills.forms import BillModelForm
from bills.models import Bill
from django.http import FileResponse,Http404
from core.view_classes import CustomCreateView, CustomUpdateView, CustomListView


class BillListView(CustomListView):
    extra_context = {
        'BILL_TYPES':BILL_TYPES,
        'BILL_STATUSES':BILL_STATUSES,
        'BILL_ORDERING_OPTIONS':BILL_ORDERING_OPTIONS,
        'BILL_PAYMENT_TYPES':BILL_PAYMENT_TYPES,
        'PAGE_SIZES':[5,10,20,30,40,50],
    }
    default_ordering = '-created_date' 
    get_queryset_function_to_eval = 'self.request.user.get_bills'


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
        fullDir = obj.get_payment_proof_fulldir()
        if not fullDir:
            raise Http404()
        fileResponse = FileResponse(
            open(fullDir,'rb')
        )
        return fileResponse
