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
    room = models.ForeignKey("Room", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.roll_no} - {self.first_name} {self.last_name}"


# -------------------------------
# Room Model
# -------------------------------
class Room(models.Model):
    ROOM_TYPES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
        ('AC', 'AC'),
        ('Non-AC', 'Non-AC'),
    )

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)

    def __str__(self):
        return f"Room {self.room_number}"

    @property
    def is_full(self):
        return self.current_occupancy >= self.capacity


# -------------------------------
# Allocation Model (History)
# -------------------------------
class Allocation(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="allocated_by")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} → Room {self.room.room_number}"


# -------------------------------
# Optional: Room Maintenance (Extra Feature)
# -------------------------------
class Maintenance(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reason = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} → Room {self.room.room_number}"

