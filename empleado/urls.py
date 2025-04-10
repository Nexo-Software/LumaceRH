from django.urls import path
from .views import PostulanteListView, PostulanteCreateView

urlpatterns = [
    path('', PostulanteListView.as_view(), name='postulante_list'),  # Listar postulantes
    path('create/', PostulanteCreateView.as_view(), name='postulante_create'),

]
