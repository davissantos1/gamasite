# Generated by Django 5.1.3 on 2024-12-18 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('Imóveis', 'Imóveis'), ('Veículos', 'Veículos'), ('Rural', 'Rural'), ('Outros Bens', 'Outros Bens')], max_length=100, unique=True, verbose_name='Nome da Categoria')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_items', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Categoria de Leilão',
                'verbose_name_plural': 'Categorias de Leilão',
            },
        ),
    ]
