from . import views
from django.urls import path

urlpatterns = [
    path('aktivitas/', views.AktivitasView.as_view(), name='aktivitas-list'),
]
