from django.urls import path
from django.contrib.auth.decorators import login_required

from bills.views import *

urlpatterns = [
    path('list/',login_required(BillListView.as_view()),name='bill_list'),
    path('create/',login_required(BillCreateView.as_view()),name='bill_create'),
    path('<int:pk>/update/',login_required(BillUpdateView.as_view()),name='bill_update'),
    path('<int:pk>/delete/',login_required(BillDeleteView.as_view()),name='bill_delete'),
]