from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'nama_depan', 'nama_belakang', 'nama_lengkap']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_email(self, value):
        if self.instance and value != self.instance.email:
            raise serializers.ValidationError('email is immutable once set.')
        return value
