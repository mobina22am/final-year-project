from django.contrib import admin
from .models import User, StoredSongs

# Registering the models here so they can be visible in the backend and also via the admin page
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'birthday', 'password')
    list_filter = ('first_name', 'birthday')
    search_fields = ('first_name', 'birthday')

@admin.register(StoredSongs)
class StoredSongsAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'instrument', 'pdfFile')

    def pdfFile(self, obj):
        if obj.pdfFile:
            return f'<a href="{obj.pdfFile.url}" target="_blank">View PDF</a>'
        return 'No PDF'

    pdfFile.allow_tags = True