from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('list/',login_required(BillCategoryListView.as_view()),name='billcategory_list')
]