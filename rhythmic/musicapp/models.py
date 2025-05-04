from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

# The model for users
class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}"

# The models for the stored songs
class StoredSongs(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    details = models.TextField()
    instrument = models.CharField(max_length=100, blank=True)

    # Store binary PDF data of the music sheet directly
    pdfFile = models.BinaryField(null=True, blank=True)  

    createdAt = models.DateTimeField(default=timezone.now)

    # Each of the stored songs are related to a user (many to one relationship)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} by {self.artist} ({self.instrument})"