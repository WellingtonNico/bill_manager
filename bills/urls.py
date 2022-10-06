from django.urls import path
from django.contrib.auth.decorators import login_required

from bills.views import *

urlpatterns = [
    path('list/',login_required(BillListView.as_view()),name='bill_list'),
    path('create/',login_required(BillCreateView.as_view()),name='bill_create'),
    path('<int:pk>/update/',login_required(BillUpdateView.as_view()),name='bill_update'),
    path('<int:pk>/pay/',login_required(BillPaymentUpdateView.as_view()),name='bill_pay'),
    path('<int:pk>/undo_payment/',login_required(BillUndoPaymentUpdateView.as_view()),name='bill_undo_payment'),
    path('<int:pk>/delete/',login_required(BillDeleteView.as_view()),name='bill_delete'),
    path('<int:pk>/payment_proof_download/',login_required(BillPaymentProofDownloadView.as_view()),name='bill_payment_proof_download'),
]