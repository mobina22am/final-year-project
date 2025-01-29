from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    birthday = models.DateField()
    password = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.name}"



class StoredSongs(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    details = models.TextField()
    notes = models.TextField()
    instrument = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name}"
    




# user = User.objects.get(id=1)  # Get the user
# song = StoredSongs.objects.get(user=user, name="Song Title")
# print(song.details)