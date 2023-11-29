from rest_framework import serializers

from .models import KegiatanPARA, Acara, Aktivitas


class KegiatanPARASerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    pemilik = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = KegiatanPARA
        fields = ['id', 'kategori', 'judul', 'deskripsi', 'lokasi', 'waktu_pengingat', 'pemilik']
        abstract = True


class AcaraSerializer(KegiatanPARASerializer):
    class Meta:
        model = Acara
        fields = [*KegiatanPARASerializer.Meta.fields, 'waktu_mulai', 'waktu_akhir']

    def validate(self, data):
        """
        Check that waktu_mulai is before waktu_akhir.
        """
        if data.get('waktu_mulai', self.instance.waktu_mulai if self.instance else None) > \
                data.get('waktu_akhir', self.instance.waktu_akhir if self.instance else None):
            raise serializers.ValidationError('waktu_akhir harus setelah waktu_awal', code='invalid_date')
        return data


class AktivitasSerializer(KegiatanPARASerializer):
    class Meta:
        model = Aktivitas
        fields = [*KegiatanPARASerializer.Meta.fields, 'tenggat_waktu']
