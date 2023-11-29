from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Aktivitas, Acara
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
