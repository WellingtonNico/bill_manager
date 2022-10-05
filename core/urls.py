from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.urls import include
from django.views.generic import RedirectView,TemplateView
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    PasswordResetCompleteView
)

from core.forms import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bills/',include('bills.urls')),
    path('bill_categories/',include('bill_categories.urls')),
    path('bill_chargers/',include('bill_chargers.urls')),
    path('',RedirectView.as_view(url=reverse_lazy('bill_list'))),


    path('login/',LoginView.as_view(form_class=CustomAuthenticationForm),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    # REGISTRAÇÃO e CONTROLE
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    # path('support',login_required(SupportView.as_view()),name='support'),
    path('support_sent_confirmation',login_required(TemplateView.as_view(template_name='support/support_sent_confirmation.html')),name='support_sent_confirmation'),
    path('support/tutorials',login_required(TemplateView.as_view(template_name='support/tutorials.html')),name='support_tutorials'),
    path('password_change/', login_required(PasswordChangeView.as_view()), name='password_change'),
    path('password_change/done/', login_required(PasswordChangeDoneView.as_view()), name='password_change_done'),
    path('password_reset/done/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/', PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html',form_class=CustomPasswordResetForm), name='password_reset'),
]
