from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from cryptography.fernet import Fernet
from django.utils.translation import gettext_lazy as _

SECRET_KEY = b'Boi62ClGGP4HforWHdJqK--dMWXcXir4GbgdHLqz7cY=' 
cipher_suite = Fernet(SECRET_KEY)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ssn = models.CharField(max_length=12)  # SSN should be encrypted and decrypted
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ssn_encrypted = models.BinaryField(editable=False)  # Store encrypted SSN as binary

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'ssn']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.ssn_encrypted = cipher_suite.encrypt(self.ssn.encode())
        # Call the decryption method before saving
        self.decrypt_ssn()
        # Clear the plain SSN after encryption to avoid storing it
        self.ssn = ""
        super().save(*args, **kwargs)

    def decrypt_ssn(self):
        # Decrypt the SSN field for validation purposes
        try:
            decrypted_ssn = cipher_suite.decrypt(self.ssn_encrypted)
            self.ssn = decrypted_ssn.decode()
        except Exception as e:
            # Handle decryption errors (e.g., invalid data)
            raise ValidationError("Invalid SSN")

    def clean(self):
        super().clean()

    def get_masked_ssn(self):
        # Decrypt the SSN and return a masked version for display in the admin
        try:
            decrypted_ssn = cipher_suite.decrypt(self.ssn_encrypted)
            return "XXX-XX-" + decrypted_ssn[-4:].decode()
        except Exception as e:
            return "Invalid SSN"

    get_masked_ssn.short_description = 'SSN'  # Customize the column header in the admin
