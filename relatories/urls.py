from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [
    path('bills/',login_required(BillRelatoryView.as_view()),name='billrelatory_view'),
    path('bills/create/',login_required(BillRelatoryCreateView.as_view()),name='billrelatory_create'),
    path('bills/<int:pk>/update/',login_required(BillRelatoryUpdateView.as_view()),name='billrelatory_update'),

]