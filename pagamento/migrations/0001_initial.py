# Generated by Django 3.2.10 on 2021-12-26 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagamento', models.CharField(max_length=30, unique=True)),
            ],
        ),
    ]
