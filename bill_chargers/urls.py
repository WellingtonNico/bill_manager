from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('list/',login_required(BillChargerListView.as_view()),name='billcharger_list'),
    path('create/',login_required(BillChargerCreateView.as_view()),name='billcharger_create'),
    path('<int:pk>/update/',login_required(BillChargerUpdateView.as_view()),name='billcharger_update'),
]