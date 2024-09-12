# Generated by Django 4.2.16 on 2024-09-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('type', models.CharField(choices=[('moderator', 'Moderator'), ('user', 'İstifadəçi')], default='user', editable=False, max_length=55, verbose_name='İstifadəçi tipi')),
                ('phone_number', models.CharField(error_messages={'unique': 'A user with that phone number already exists.'}, max_length=40, unique=True, verbose_name='Telefon nömrəsi')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('first_name', models.CharField(default='', max_length=30, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=150, verbose_name='Last Name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='date joined')),
                ('last_password_forgot_request', models.DateTimeField(auto_now_add=True, verbose_name='Last password request date')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
