from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Aktivitas
from .serializers import AktivitasSerializer


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
