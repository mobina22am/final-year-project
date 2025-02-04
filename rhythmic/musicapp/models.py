from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}"

class StoredSongs(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    details = models.TextField()
    notes = models.TextField()
    instrument = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return f"{self.name}"
    




# user = User.objects.get(id=1)  # Get the user
# song = StoredSongs.objects.get(user=user, name="Song Title")
# print(song.details)