# Generated by Django 3.2.10 on 2022-03-18 03:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='codigo_de_convite',
            field=models.UUIDField(default=uuid.UUID('1302411e-d2d1-49ca-b3a4-c40b5e7f6114'), unique=True),
        ),
    ]