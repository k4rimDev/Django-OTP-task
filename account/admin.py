from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from account import models
from base_user.models import MyUser as MUser
from base_user.forms import MyUserChangeForm, MyUserCreationForm


admin.site.register(models.Moderator)
admin.site.register(MUser)


class RegularUserMoreAdmin(admin.StackedInline):
    model = models.RegularUserMore


@admin.register(models.RegularUser)
class RegularUserAdmin(admin.ModelAdmin):
    inlines = [RegularUserMoreAdmin]
    search_fields = ['regular_user_fields__phone', 'first_name']
    list_filter = ['is_active']
    add_form = MyUserCreationForm
    form = MyUserChangeForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during foo creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
