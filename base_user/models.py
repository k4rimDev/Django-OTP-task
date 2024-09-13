from django.contrib.auth.base_user import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings


USER_MODEL = settings.AUTH_USER_MODEL


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, phone_number, password, **extra_fields):
        """
        Create and save a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError(_('The Phone number must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given phone_number and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone_number, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        MODERATOR = "moderator", _('Moderator')
        USER = "user", _('İstifadəçi')

    type = models.CharField(_('İstifadəçi tipi'), max_length=55, choices=Types.choices, default=Types.USER,
                            editable=False)

    phone_number = models.CharField(_('Telefon nömrəsi'), max_length=40, unique=True, error_messages={
        'unique': _("A user with that phone number already exists."),
    })

    email = models.EmailField(_('Email'), max_length=100, unique=False)

    first_name = models.CharField(_('First Name'), max_length=30, default='')
    last_name = models.CharField(_('Last Name'), max_length=150, default='')

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'), )
    date_joined = models.DateTimeField(_('date joined'), auto_now=True)
    last_password_forgot_request = models.DateTimeField(_('Last password request date'), auto_now_add=True)

    objects = CustomUserManager()
    EMAIL_FIELD = 'phone_number'
    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @property
    def user_fields_by_type(self):
        if self.type == self.Types.USER:
            return self.regular_user_fields
        return None

    def __str__(self):
        try:
            return f'Ad : {self.first_name} - - - Tel : {self.user_fields_by_type.phone} - - - Istifadəçi tipi : {self.get_type_display()}'
        except:
            return f'{self.get_type_display()} : {self.first_name}, {self.phone_number}'

User = MyUser()
