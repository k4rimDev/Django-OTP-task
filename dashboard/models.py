import mimetypes

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse

from services.uploader import Uploader


User = get_user_model()


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class File(models.Model):
    FILE_TYPES = [
        ('PNG', '.png'),
        ('DOC', '.doc'),
        ('PPTX', '.pptx')
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=Uploader.upload_file)
    file_type = models.CharField(max_length=4, choices=FILE_TYPES)
    description = models.TextField(blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='files')
    public = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    unique_link = models.CharField(max_length=255, unique=True, blank=True, null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file.name} owned by {self.owner.email}"
    
    def save(self, *args, **kwargs):
        if self.file:
            mime_type, _ = mimetypes.guess_type(self.file.name)
            if mime_type:
                if 'png' in mime_type:
                    self.file_type = 'PNG'
                elif 'msword' in mime_type or 'vnd.openxmlformats-officedocument.wordprocessingml.document' in mime_type:
                    self.file_type = 'DOC'
                elif 'vnd.openxmlformats-officedocument.presentationml.presentation' in mime_type:
                    self.file_type = 'PPTX'
        
        super().save(*args, **kwargs)

    def generate_unique_link(self):
        self.unique_link = get_random_string(32)
        self.save()

    def increment_views(self):
        cache_key = f'file_{self.id}_views'
        if cache.get(cache_key) is None:
            cache.set(cache_key, self.views, timeout=None)
        cache.incr(cache_key)

    def get_views(self):
        cache_key = f'file_{self.id}_views'
        return cache.get(cache_key, self.views)

    def has_expired(self):
        return self.expiration_date and timezone.now() > self.expiration_date

    def delete_if_expired(self):
        if self.has_expired():
            self.delete()

    def get_absolute_url(self):
        return reverse('file-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.email} on {self.file.file.name}"

    def delete_comment(self):
        if self.user == self.file.owner or self.user == self:
            self.delete()

    class Meta:
        ordering = ['-created_at']
