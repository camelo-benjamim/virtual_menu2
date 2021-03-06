# Generated by Django 3.2.10 on 2022-03-27 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mesa', '0001_initial'),
        ('menu', '0001_initial'),
        ('pagamento', '0002_auto_20220326_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('data', models.DateTimeField(auto_now=True)),
                ('session_key', models.TextField()),
                ('concluido', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.item')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_do_pedido', models.TimeField(auto_now_add=True)),
                ('session_key', models.TextField()),
                ('concluido', models.BooleanField(default=False)),
                ('finalizado', models.BooleanField(default=False, null=True)),
                ('pedido_data_relatorio', models.DateField(auto_now_add=True, null=True)),
                ('nome_do_cliente', models.CharField(default=None, max_length=120, null=True)),
                ('mesa_pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mesa.mesa')),
                ('metodo_de_pagamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pagamento.metodosdepagamento')),
                ('pedido', models.ManyToManyField(to='carrinho.Pedido')),
            ],
            options={
                'verbose_name': 'Carrinho',
                'verbose_name_plural': 'Carrinhos',
            },
        ),
    ]
