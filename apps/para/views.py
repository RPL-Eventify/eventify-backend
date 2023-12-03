from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView ,get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from .models import Aktivitas, Acara, KegiatanPARA, KegiatanPARAManager
from .permission import IsCurrentUserOrReadOnly
from .serializers import AktivitasSerializer, AcaraSerializer, KegiatanPARASerializer


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


class AcaraDetailView(RetrieveAPIView):
    serializer_class = AcaraSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            acara = Acara.objects.get(id=id_param)
            self.check_object_permissions(self.request, acara)
            return acara
        except Acara.DoesNotExist:
            raise NotFound(f"Acara dengan id {id_param} tidak ditemukan", code="Acara_Not_Found")

class ArchiveKegiatanView(APIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def post(self, request, id):
        kegiatan = self.get_kegiatan(id)
        kegiatan.archived()
        return Response({'status': 'Kegiatan archived successfully'}, status=status.HTTP_200_OK)

    def get_kegiatan(self, id):
        try:
            return Acara.objects.get(id=id)
        except Acara.DoesNotExist:
            try:
                return Aktivitas.objects.get(id=id)
            except Aktivitas.DoesNotExist:
                raise NotFound(f"Kegiatan dengan id {id} tidak ditemukan", code="Kegiatan_Not_Found")


class UnarchiveKegiatanView(APIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def post(self, request, id):
        kegiatan = self.get_kegiatan(id)
        kegiatan.unarchived()
        return Response({'status': 'Kegiatan unarchived successfully'}, status=status.HTTP_200_OK)

    def get_kegiatan(self, id):
        try:
            return Acara.objects.get(id=id)
        except Acara.DoesNotExist:
            try:
                return Aktivitas.objects.get(id=id)
            except Aktivitas.DoesNotExist:
                raise NotFound(f"Kegiatan dengan id {id} tidak ditemukan", code="Kegiatan_Not_Found")

class DeleteKegiatanView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def delete(self, request, id):
        instance = self.get_object(id)
        self.perform_destroy(instance)
        return Response({'status': 'Kegiatan deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, id):
        try:
            return Acara.objects.get(id=id)
        except Acara.DoesNotExist:
            try:
                return Aktivitas.objects.get(id=id)
            except Aktivitas.DoesNotExist:
                raise NotFound(f"Kegiatan dengan id {id} tidak ditemukan", code="Kegiatan_Not_Found")