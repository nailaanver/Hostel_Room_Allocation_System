from django.contrib.auth.models import User
from django.db import models

DEPARTMENT_CHOICES = (
    ('BCA', 'BCA'),
    ('BCom', 'BCom'),
    ('BA English', 'BA English'),
    ('BSc CS', 'BSc Computer Science'),
    ('BBA', 'BBA'),
)

YEAR_CHOICES = (
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    roll_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile_no = models.CharField(max_length=15)

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    year_of_study = models.CharField(max_length=10, choices=YEAR_CHOICES)

    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.roll_no} - {self.first_name} {self.last_name}"
