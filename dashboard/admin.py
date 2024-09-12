from django.contrib import admin

from dashboard.models import File, Comment, Hashtag



@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'owner', 'file_type', 'public', 'views', 'expiration_date', 'created_at')
    list_filter = ('public', 'file_type', 'expiration_date', 'created_at')
    search_fields = ('file__name', 'description', 'owner__email')
    ordering = ('-created_at',)

    def file_name(self, obj):
        return obj.file.name


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('file__file', 'user__email', 'text')
    ordering = ('-created_at',)


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
