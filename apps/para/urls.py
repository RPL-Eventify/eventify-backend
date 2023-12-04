from . import views
from django.urls import path

urlpatterns = [
    path('aktivitas/', views.AktivitasView.as_view(), name='aktivitas-list'),
    path('acara/', views.AcaraView.as_view(), name='acara-list'),
    path('aktivitas/<uuid:id>/', views.AktivitasDetailView.as_view(), name='aktivitas-detail'),
    path('acara/<uuid:id>/', views.AcaraDetailView.as_view(), name='acara-detail'),
    path('archived/aktivitas/', views.ArchivedAktivitasListView.as_view(), name='archived-aktivitas-list'),
    path('archived/acara/', views.ArchivedAcaraListView.as_view(), name='archived-acara-list'),
    path('aktivitas/<uuid:id>/archive/', views.ArchiveAktivitasView.as_view(), name='archive-aktivitas'),
    path('acara/<uuid:id>/archive/', views.ArchiveAcaraView.as_view(), name='archive-acara'),
    path('aktivitas/<uuid:id>/unarchive/', views.UnarchiveAktivitasView.as_view(), name='unarchive-aktivitas'),
    path('acara/<uuid:id>/unarchive/', views.UnarchiveAcaraView.as_view(), name='unarchive-acara'),
    path('archived/aktivitas/<uuid:id>/delete/', views.AktivitasDeleteView.as_view(), name='archived-aktivitas-delete'),
    path('archived/acara/<uuid:id>/delete/', views.AcaraDeleteView.as_view(), name='archived-acara-delete'),
]
