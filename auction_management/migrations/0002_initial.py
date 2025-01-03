# Generated by Django 5.1.3 on 2024-12-27 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auction_management', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='othergoods',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='other_goods_bids', to='payment.bid', verbose_name='Lances'),
        ),
        migrations.AddField(
            model_name='othergoods',
            name='imagens',
            field=models.ManyToManyField(related_name='other_goods_imagens', to='auction_management.itemimage'),
        ),
        migrations.AddField(
            model_name='othergoods',
            name='leilao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_goods', to='auction_management.auction', verbose_name='Leilão'),
        ),
        migrations.AddField(
            model_name='othergoods',
            name='tipo_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auction_management.itemtype', verbose_name='Tipo do Item'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='other_goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagens_othergoods', to='auction_management.othergoods'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='real_estate_bids', to='payment.bid', verbose_name='Lances'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='imagens',
            field=models.ManyToManyField(related_name='real_estate_imagens', to='auction_management.itemimage'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='leilao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='real_estates', to='auction_management.auction', verbose_name='Leilão'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='tipo_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auction_management.itemtype', verbose_name='Tipo do Item'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='real_estate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagens_realestate', to='auction_management.realestate'),
        ),
        migrations.AddField(
            model_name='ruralitem',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='rural_item_bids', to='payment.bid', verbose_name='Lances'),
        ),
        migrations.AddField(
            model_name='ruralitem',
            name='imagens',
            field=models.ManyToManyField(related_name='rural_item_imagens', to='auction_management.itemimage'),
        ),
        migrations.AddField(
            model_name='ruralitem',
            name='leilao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rural_items', to='auction_management.auction', verbose_name='Leilão'),
        ),
        migrations.AddField(
            model_name='ruralitem',
            name='tipo_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auction_management.itemtype', verbose_name='Tipo do Item'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='rural_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagens_ruralitem', to='auction_management.ruralitem'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='vehicle_bids', to='payment.bid', verbose_name='Lances'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='imagens',
            field=models.ManyToManyField(related_name='vehicle_imagens', to='auction_management.itemimage'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='leilao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='auction_management.auction', verbose_name='Leilão'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='tipo_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auction_management.itemtype', verbose_name='Tipo do Item'),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagens_vehicle', to='auction_management.vehicle'),
        ),
    ]
