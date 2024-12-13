# Generated by Django 5.1.3 on 2024-12-13 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_management', '0008_realestate_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='othergoods',
            name='imagem',
            field=models.ImageField(default='default/default_image.jpg', upload_to='outros_bens/'),
        ),
        migrations.AddField(
            model_name='ruralitem',
            name='imagem',
            field=models.ImageField(default='default/default_image.jpg', upload_to='rural/'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='imagem',
            field=models.ImageField(default='default/default_image.jpg', upload_to='imoveis/'),
        ),
    ]