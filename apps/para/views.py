from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import Aktivitas, Acara
from .permission import IsCurrentUserOrReadOnly
from .serializers import AktivitasSerializer, AcaraSerializer


# Create your views here.
class AktivitasView(ListCreateAPIView):
    serializer_class = AktivitasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategori']

    def get_queryset(self):
        user = self.request.user
        return Aktivitas.objects.filter(pemilik=user)

    def perform_create(self, serializer):
        serializer.save(pemilik=self.request.user)

class AcaraView(ListCreateAPIView):
    serializer_class = AcaraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategori']

    def get_queryset(self):
        user = self.request.user
        return Acara.objects.filter(pemilik=user)

    def perform_create(self, serializer):
        serializer.validated_data['kategori'] = 'projects'
        serializer.save(pemilik=self.request.user)

class AktivitasDetailView(RetrieveAPIView):
    serializer_class = AktivitasSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            aktivitas = Aktivitas.objects.get(id=id_param)
            self.check_object_permissions(self.request, aktivitas)
            return aktivitas
        except Aktivitas.DoesNotExist:
            raise NotFound(f"Aktivitas dengan id {id_param} tidak ditemukan", code="Activity_Not_Found")
