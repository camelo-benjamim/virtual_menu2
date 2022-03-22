# Generated by Django 3.2.10 on 2022-03-20 03:09

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('postal_code', models.IntegerField(default=0)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(choices=[('AC', 'ACRE'), ('AL', 'ALAGOAS'), ('AM', 'AMAPÁ'), ('AZ', 'AMAZONAS'), ('BA', 'BAHIA'), ('CE', 'CEARÁ'), ('DF', 'DISTRITO FEDERAL'), ('ES', 'ESPIRITO SANTO'), ('GO', 'GOIÁS'), ('MA', 'MARANHÃO'), ('MT', 'MATO GROSSO'), ('MS', 'MATO GROSSO DO SUL'), ('MG', 'MINAS GERAIS'), ('PA', 'PARÁ'), ('PB', 'PARAÍBA'), ('PN', 'PARANÁ'), ('PE', 'PERNAMBUCO'), ('PI', 'PIAUÍ'), ('RJ', 'RIO DE JANEIRO'), ('RN', 'RIO GRANDE DO NORTE'), ('RS', 'RIO GRANDE DO SUL'), ('RO', 'RONDÔNIA'), ('RM', 'RORAIMA'), ('SC', 'SANTA CATARINA'), ('SP', 'SÃO PAULO'), ('SE', 'SERGIPE'), ('TO', 'TOCANTINS')], max_length=2)),
                ('address', models.CharField(max_length=40)),
                ('district', models.CharField(max_length=40)),
                ('number_ref', models.SmallIntegerField(default=0)),
                ('contacts_phone', models.BigIntegerField(default=0, unique=True)),
                ('avatar', models.ImageField(blank=True, default=None, null=True, upload_to='avatar/')),
                ('codigo_de_convite', models.CharField(max_length=32, unique=True)),
                ('codigo_convidado', models.CharField(default=None, max_length=120, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
