# Generated by Django 5.1.3 on 2024-12-18 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_alter_documento_tipo_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='status',
            field=models.CharField(choices=[('P', 'Pendente'), ('A', 'Aprovado'), ('R', 'Rejeitado')], default='P', max_length=1),
        ),
    ]
