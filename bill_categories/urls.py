from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('list/',login_required(BillCategoryListView.as_view()),name='billcategory_list'),
    path('create/',login_required(BillCategoryCreateView.as_view()),name='billcategory_create'),
    path('<int:pk>/update/',login_required(BillCategoryUpdateView.as_view()),name='billcategory_update'),
]