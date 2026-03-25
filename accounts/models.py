from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


# custom manager(to call objects in view)
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 1)

        return self.create_user(email, password, **extra_fields)


# custom user
class CustomUser(AbstractUser):
    username = None   
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        (1, 'Admin'),
        (2, 'Vendor'),
        (3, 'User'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()   

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"


# vendor
class Vendor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True, null=True)

    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    certificate = models.FileField(upload_to='vendor/certificates/', blank=True, null=True)
    id_proof = models.FileField(upload_to='vendor/id_proofs/', blank=True, null=True)

    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vendor: {self.full_name} ({self.user.email})"


# vendor-request
class VendorRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    bio = models.TextField(blank=True, null=True)

    experience_years = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    certificate = models.FileField(upload_to='vendor_requests/certificates/', blank=True, null=True)
    id_proof = models.FileField(upload_to='vendor_requests/id_proofs/', blank=True, null=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_remark = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"