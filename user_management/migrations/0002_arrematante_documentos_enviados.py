# Generated by Django 5.1.3 on 2025-01-02 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrematante',
            name='documentos_enviados',
            field=models.BooleanField(default=False),
        ),
    ]
