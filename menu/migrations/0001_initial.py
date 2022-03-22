# Generated by Django 3.2.10 on 2022-03-20 01:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classificacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_classificacao', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Classificação',
                'verbose_name_plural': 'Classificações',
            },
        ),
        migrations.CreateModel(
            name='Restaurante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_restaurante', models.CharField(max_length=125)),
                ('logo_restaurante', models.ImageField(blank=True, default=None, null=True, upload_to='logo_restaurantes/')),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proprietario_restaurante', to=settings.AUTH_USER_MODEL)),
                ('usuario_criador', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item_classificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=40)),
                ('classificacao', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='menu.classificacoes')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_nome', models.CharField(max_length=40)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('img', models.ImageField(blank=True, default=None, null=True, upload_to='images/')),
                ('classificacao', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='menu.item_classificacao')),
            ],
            options={
                'verbose_name_plural': 'Itens',
            },
        ),
        migrations.AddField(
            model_name='classificacoes',
            name='restaurante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.restaurante'),
        ),
    ]
