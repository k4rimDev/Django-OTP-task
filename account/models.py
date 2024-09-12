from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

from base_user.models import MyUser


class ModeratorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MyUser.Types.MODERATOR)


class RegularUserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=MyUser.Types.USER)


class Moderator(MyUser):
    objects = ModeratorManager()

    class Meta:
        proxy = True
        verbose_name = _('Moderator')
        verbose_name_plural = _('Moderatorlar')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MyUser.Types.MODERATOR

        return super().save(*args, **kwargs)


class RegularUser(MyUser):
    objects = RegularUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Sadə İstifadəçi')
        verbose_name_plural = _('Sadə İstifadəçilər')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = MyUser.Types.USER

        return super().save(*args, **kwargs)

    @property
    def additional(self):
        return self.regular_user_fields


class RegularUserMore(models.Model):
    user = models.OneToOneField(RegularUser, on_delete=models.CASCADE, related_name='regular_user_fields')

    def __str__(self):
        return f'{self.user.id}'
