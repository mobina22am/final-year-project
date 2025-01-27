from django.contrib import admin
from .models import User, StoredSongs

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'birthday', 'password')
    list_filter = ('name', 'birthday')
    search_fields = ('name', 'birthday')


@admin.register(StoredSongs)
class StoredSongsAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'details', 'notes')
    list_filter = ('name', 'artist', 'details')
    search_fields = ('name', 'artist', 'details')