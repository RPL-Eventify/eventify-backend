import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError('Email cannot be empty')

        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        user = self.create_user(email, password=password, **other_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True)
    nama_depan = models.CharField(max_length=100)
    nama_belakang = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Manager
    objects = UserManager()

    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nama_depan', 'nama_belakang']

    def __str__(self):
        return self.nama_depan

    @property
    def nama_lengkap(self):
        """
        Return the person's full name.
        """
        return f'{self.nama_depan} {self.nama_belakang}'
