from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListAPIView, \
    RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from .models import Aktivitas, Acara
from .permission import IsCurrentUserOrReadOnly
from .serializers import AktivitasSerializer, AcaraSerializer
from rest_framework.response import Response


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
        tenggat_waktu = self.request.data.get('tenggat_waktu')
        kategori = self.request.data.get('kategori')
        if kategori == 'projects' and not tenggat_waktu:
            raise ParseError(f"Tenggat Waktu tidak boleh kosong", code="Empty_Tenggat_Waktu")
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


class AktivitasDeleteView(RetrieveDestroyAPIView):
    serializer_class = AktivitasSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            aktivitas = Aktivitas.objects.get_archived_queryset().get(id=id_param)
            self.check_object_permissions(self.request, aktivitas)
            return aktivitas
        except Aktivitas.DoesNotExist:
            try:
                aktivitas = Aktivitas.objects.get_queryset().get(id=id_param)
                if not aktivitas.is_archived:
                    raise ParseError(f"Aktivitas dengan id {id_param} tidak di-archive", code="Aktivitas_Not_Archived")
            except Aktivitas.DoesNotExist:
                raise NotFound(f"Aktivitas dengan id {id_param} tidak ditemukan", code="Aktivitas_Not_Found")

    def destroy(self, request, *args, **kwargs):
        aktivitas = self.get_object()
        self.perform_destroy(aktivitas)
        return Response({"detail": "Aktivitas berhasil dihapus"}, status=status.HTTP_200_OK)


class AcaraDeleteView(RetrieveDestroyAPIView):
    serializer_class = AcaraSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        id_param = self.kwargs.get('id')
        try:
            acara = Acara.objects.get_archived_queryset().get(id=id_param)
            self.check_object_permissions(self.request, acara)
            return acara
        except Acara.DoesNotExist:
            try:
                acara = Acara.objects.get_queryset().get(id=id_param)
                if not acara.is_archived:
                    raise ParseError(f"Acara dengan id {id_param} tidak di-archive", code="Acara_Not_Archived")
            except Acara.DoesNotExist:
                raise NotFound(f"Acara dengan id {id_param} tidak ditemukan", code="Acara_Not_Found")

    def destroy(self, request, *args, **kwargs):
        acara = self.get_object()
        self.perform_destroy(acara)
        return Response({"detail": "Acara berhasil dihapus"}, status=status.HTTP_200_OK)