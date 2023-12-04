from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
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


class ArchiveAktivitasView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]
    serializer_class = AktivitasSerializer

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            aktivitas = Aktivitas.objects.get(id=id_param)
            self.check_object_permissions(self.request, aktivitas)
            return aktivitas
        except Aktivitas.DoesNotExist:
            raise NotFound(f"Aktivitas dengan id {id_param} tidak ditemukan", code="Kegiatan_Not_Found")

    def partial_update(self, request, *args, **kwargs):
        aktivitas = self.get_object()
        aktivitas.archived()
        serializer = self.get_serializer(aktivitas, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UnarchiveAktivitasView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]
    serializer_class = AktivitasSerializer

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            aktivitas = Aktivitas.objects.get_archived_queryset().get(id=id_param)
            self.check_object_permissions(self.request, aktivitas)
            return aktivitas
        except Aktivitas.DoesNotExist:
            raise NotFound(f"Aktivitas dengan id {id_param} tidak ditemukan", code="Kegiatan_Not_Found")

    def partial_update(self, request, *args, **kwargs):
        aktivitas = self.get_object()
        aktivitas.unarchived()
        serializer = self.get_serializer(aktivitas, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ArchiveAcaraView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]
    serializer_class = AcaraSerializer

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            acara = Acara.objects.get(id=id_param)
            self.check_object_permissions(self.request, acara)
            return acara
        except Acara.DoesNotExist:
            raise NotFound(f"Acara dengan id {id_param} tidak ditemukan", code="Kegiatan_Not_Found")

    def partial_update(self, request, *args, **kwargs):
        acara = self.get_object()
        acara.archived()
        serializer = self.get_serializer(acara, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UnarchiveAcaraView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]
    serializer_class = AcaraSerializer

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            acara = Acara.objects.get_archived_queryset().get(id=id_param)
            self.check_object_permissions(self.request, acara)
            return acara
        except Acara.DoesNotExist:
            raise NotFound(f"Acara dengan id {id_param} tidak ditemukan", code="Kegiatan_Not_Found")

    def partial_update(self, request, *args, **kwargs):
        acara = self.get_object()
        acara.unarchived()
        serializer = self.get_serializer(acara, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ArchivedAktivitasListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AktivitasSerializer

    def get_queryset(self):
        user = self.request.user
        return Aktivitas.objects.get_archived_queryset().filter(pemilik=user)


class ArchivedAcaraListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AcaraSerializer

    def get_queryset(self):
        user = self.request.user
        return Acara.objects.get_archived_queryset().filter(pemilik=user)
