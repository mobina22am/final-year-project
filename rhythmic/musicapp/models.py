from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    birthday = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)


    # this is to prevent any errors for overriding the abstract class
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True
    )


    def __str__(self):
        return f"{self.name}"

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