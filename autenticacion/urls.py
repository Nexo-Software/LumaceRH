from django.urls import path, re_path, include
from allauth.account.views import LogoutView
from .views import MyCustomSignupView, MyCustomLoginView

urlpatterns = [
    path('registrar/', MyCustomSignupView.as_view(), name='account_signup'),
    path('iniciar/', MyCustomLoginView.as_view(), name='account_login'),
    path('cerrar/', LogoutView.as_view(), name='account_logout'),
]