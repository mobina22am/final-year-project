from django.db import models

# Create your models here.

class User(models.Model):
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


    def __str__(self):
        return f"{self.name}"