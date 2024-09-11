from django.db import models
from django.conf import settings

from files.models import File


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def delete_comment(self):
        if self.user == self.file.owner or self.user == self:
            self.delete()
