# Generated by Django 5.1.3 on 2024-12-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='tipo_documento',
            field=models.CharField(choices=[('RG', 'RG'), ('CNH', 'CNH'), ('PASSAPORTE', 'Passaporte'), ('COMPROVANTE_RESIDENCIA', 'Comprovante de Residência'), ('CONTRATO_SOCIAL', 'Contrato Social'), ('SELFIE', 'Selfie')], max_length=50),
        ),
    ]
