from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

ROLE_CHOICES = [
    ('employee', 'Employee'),
    ('manager', 'Manager'),
]

STATUS_CHOICES = [
    ('WIP', 'Work in Progress'),
    ('DONE', 'Done'),
    ('HOLD', 'Hold'),
]


class UserManager(BaseUserManager):
    def create_user(self, office_email, password=None, **extra_fields):
        if not office_email:
            raise ValueError("Email is required")
        email = self.normalize_email(office_email)
        user = self.model(office_email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, office_email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(office_email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    office_email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'office_email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.office_email})"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    priority = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    task = models.CharField(max_length=255)
    details = models.TextField()
    target_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    live = models.CharField(max_length=100, blank=True)
    tested = models.CharField(max_length=100, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.task}"
