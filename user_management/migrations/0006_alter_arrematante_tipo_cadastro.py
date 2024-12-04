# Generated by Django 5.1.3 on 2024-12-04 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0005_alter_arrematante_cpf_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrematante',
            name='tipo_cadastro',
            field=models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2),
        ),
    ]
