from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.cache import cache


class File(models.Model):
    FILE_TYPES = [
        ('PNG', '.png'),
        ('DOC', '.doc'),
        ('PPTX', '.pptx')
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=4, choices=FILE_TYPES)
    description = models.TextField(blank=True, null=True)
    hashtags = models.ManyToManyField('Hashtag')
    public = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    unique_link = models.CharField(max_length=255, unique=True, blank=True, null=True)
    views = models.IntegerField(default=0)

    def generate_unique_link(self):
        self.unique_link = get_random_string(32)

    def increment_views(self):
        cache.incr(f'file_{self.id}_views')
    
    def get_views(self):
        return cache.get(f'file_{self.id}_views', self.views)
