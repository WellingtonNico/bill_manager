from django.urls import path
from django.contrib.auth.decorators import login_required

from bills.views import BillListView

urlpatterns = [
    path('list/',login_required(BillListView.as_view()),name='bill_list')
]