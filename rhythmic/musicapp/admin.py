from django.contrib import admin
from .models import User, StoredSongs

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'birthday', 'password')
    list_filter = ('first_name', 'birthday')
    search_fields = ('first_name', 'birthday')


@admin.register(StoredSongs)
class StoredSongsAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'details', 'notes', 'instrument', 'created_at', 'user')
    list_filter = ('name', 'artist', 'details', 'instrument', 'created_at', 'user')
    search_fields = ('name', 'artist', 'details', 'instrument', 'created_at', 'user')