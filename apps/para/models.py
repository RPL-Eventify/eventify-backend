import uuid

from django.db import models

from apps.user.models import User


# Create your models here.
class KegiatanPARAManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(self.model, using=self._db).exclude(is_archived=True)

    def get_archived_queryset(self):
        return models.QuerySet(self.model, using=self._db).filter(is_archived=True)


class KegiatanPARA(models.Model):
    class Meta:
        abstract = True

    KEGIATAN_CHOICES = [
        ('projects', 'projects'),
        ('areas', 'areas'),
        ('resources', 'resources'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kategori = models.CharField(max_length=100, choices=KEGIATAN_CHOICES)
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, default='')
    is_archived = models.BooleanField(default=False)
    lokasi = models.CharField(max_length=100, blank=True, default='')
    waktu_pengingat = models.DateTimeField(blank=True, null=True)
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daftar_kegiatan')

    objects = KegiatanPARAManager()

    def archived(self):
        self.is_archived = True
        self.save()

    def unarchived(self):
        self.is_archived = False
        self.save()


class Acara(KegiatanPARA):
    waktu_mulai = models.DateTimeField()
    waktu_akhir = models.DateTimeField()
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daftar_acara')


class Aktivitas(KegiatanPARA):
    tenggat_waktu = models.DateTimeField(blank=True, null=True)
    pemilik = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daftar_aktivitas')
