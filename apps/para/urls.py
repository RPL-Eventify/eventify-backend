from . import views
from django.urls import path

urlpatterns = [
    path('aktivitas/', views.AktivitasView.as_view(), name='aktivitas-list'),
    path('acara/', views.AcaraView.as_view(), name='acara-list'),
    path('aktivitas/<uuid:id>/', views.AktivitasDetailView.as_view(), name='aktivitas-detail'),
    path('acara/<uuid:id>/', views.AcaraDetailView.as_view(), name='acara-detail'),
    path('archive/<uuid:id>/', views.ArchiveKegiatanView.as_view(), name='archive-kegiatan'),
    path('unarchive/<uuid:id>/', views.UnarchiveKegiatanView.as_view(), name='unarchive-kegiatan'),
    path('delete/<uuid:id>/', views.DeleteKegiatanView.as_view(), name='unarchive-kegiatan'),
]
