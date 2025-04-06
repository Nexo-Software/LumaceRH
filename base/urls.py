from django.urls import path, include
from .views import DashboardView, AppView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('apps/', AppView.as_view(), name='apps'),
]
