# Generated by Django 5.1.3 on 2024-12-03 20:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_profile_delete_cliente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(max_length=100, verbose_name='Setor')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone de Contato')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Arrematante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cadastro', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Cadastro')),
                ('cpf_cnpj', models.CharField(max_length=18, verbose_name='CPF/CNPJ')),
                ('logradouro', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=50, verbose_name='Estado')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('pais', models.CharField(max_length=50, verbose_name='País')),
                ('telefone_celular', models.CharField(max_length=15, verbose_name='Telefone Celular')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='arrematante', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_cadastro', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Cadastro')),
                ('cpf_cnpj', models.CharField(max_length=18, verbose_name='CPF/CNPJ')),
                ('logradouro', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=50, verbose_name='Estado')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('pais', models.CharField(max_length=50, verbose_name='País')),
                ('telefone_comercial', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone Comercial')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendedor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
