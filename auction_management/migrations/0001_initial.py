# Generated by Django 5.1.3 on 2024-12-20 18:32

import auction_management.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to=auction_management.models.generate_item_image_path, verbose_name='Imagem do Item')),
                ('descricao', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descrição da Imagem')),
            ],
            options={
                'verbose_name': 'Imagem do Item',
                'verbose_name_plural': 'Imagens dos Itens',
            },
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('Veículo', 'Veículo'), ('Imóvel', 'Imóvel'), ('Outros', 'Outros')], max_length=100, unique=True, verbose_name='Nome do Tipo de Item')),
            ],
            options={
                'verbose_name': 'Tipo de Item',
                'verbose_name_plural': 'Tipos de Itens',
            },
        ),
        migrations.CreateModel(
            name='OtherGoods',
            fields=[
                ('nome', models.CharField(default='Item', max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(default='sem descrição', verbose_name='Descrição')),
                ('valor_avaliado', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor Avaliado')),
                ('codigo_item', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Código do Item')),
                ('valor_arrematado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor Arrematado')),
                ('status_lote', models.CharField(choices=[('aceitando_lances', 'Aceitando lances'), ('arrematado', 'Arrematado'), ('pendente_de_pagamento', 'Pendente de pagamento')], default='aceitando_lances', max_length=50, verbose_name='Status do Lote')),
                ('status_pagamento', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente', max_length=50, verbose_name='Status de Pagamento')),
                ('destacado', models.BooleanField(default=False, verbose_name='Item Destacado')),
                ('thumbnail', models.ImageField(default='default/default_image.jpg', upload_to=auction_management.models.generate_item_thumb_path)),
            ],
            options={
                'verbose_name': 'Outro Bem',
                'verbose_name_plural': 'Outros Bens',
            },
        ),
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('nome', models.CharField(default='Item', max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(default='sem descrição', verbose_name='Descrição')),
                ('valor_avaliado', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor Avaliado')),
                ('codigo_item', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Código do Item')),
                ('valor_arrematado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor Arrematado')),
                ('status_lote', models.CharField(choices=[('aceitando_lances', 'Aceitando lances'), ('arrematado', 'Arrematado'), ('pendente_de_pagamento', 'Pendente de pagamento')], default='aceitando_lances', max_length=50, verbose_name='Status do Lote')),
                ('status_pagamento', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente', max_length=50, verbose_name='Status de Pagamento')),
                ('destacado', models.BooleanField(default=False, verbose_name='Item Destacado')),
                ('thumbnail', models.ImageField(default='default/default_image.jpg', upload_to=auction_management.models.generate_item_thumb_path)),
                ('quartos', models.IntegerField(verbose_name='Quartos')),
                ('metragem', models.FloatField(verbose_name='Metragem')),
                ('localizacao', models.CharField(max_length=255, verbose_name='Localização')),
                ('estado_imovel', models.CharField(max_length=50, verbose_name='Estado do Imóvel')),
            ],
            options={
                'verbose_name': 'Imóvel',
                'verbose_name_plural': 'Imóveis',
            },
        ),
        migrations.CreateModel(
            name='RuralItem',
            fields=[
                ('nome', models.CharField(default='Item', max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(default='sem descrição', verbose_name='Descrição')),
                ('valor_avaliado', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor Avaliado')),
                ('codigo_item', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Código do Item')),
                ('valor_arrematado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor Arrematado')),
                ('status_lote', models.CharField(choices=[('aceitando_lances', 'Aceitando lances'), ('arrematado', 'Arrematado'), ('pendente_de_pagamento', 'Pendente de pagamento')], default='aceitando_lances', max_length=50, verbose_name='Status do Lote')),
                ('status_pagamento', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente', max_length=50, verbose_name='Status de Pagamento')),
                ('destacado', models.BooleanField(default=False, verbose_name='Item Destacado')),
                ('thumbnail', models.ImageField(default='default/default_image.jpg', upload_to=auction_management.models.generate_item_thumb_path)),
                ('origem', models.CharField(default='Rural', max_length=50, verbose_name='Origem')),
            ],
            options={
                'verbose_name': 'Item Rural',
                'verbose_name_plural': 'Itens Rurais',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('nome', models.CharField(default='Item', max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(default='sem descrição', verbose_name='Descrição')),
                ('valor_avaliado', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor Avaliado')),
                ('codigo_item', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Código do Item')),
                ('valor_arrematado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor Arrematado')),
                ('status_lote', models.CharField(choices=[('aceitando_lances', 'Aceitando lances'), ('arrematado', 'Arrematado'), ('pendente_de_pagamento', 'Pendente de pagamento')], default='aceitando_lances', max_length=50, verbose_name='Status do Lote')),
                ('status_pagamento', models.CharField(choices=[('pendente', 'Pendente'), ('pago', 'Pago')], default='pendente', max_length=50, verbose_name='Status de Pagamento')),
                ('destacado', models.BooleanField(default=False, verbose_name='Item Destacado')),
                ('thumbnail', models.ImageField(default='default/default_image.jpg', upload_to=auction_management.models.generate_item_thumb_path)),
                ('versao', models.CharField(max_length=100, verbose_name='Versão')),
                ('fabricacao', models.IntegerField(verbose_name='Ano de Fabricação')),
                ('marca', models.CharField(max_length=50, verbose_name='Marca')),
                ('modelo', models.CharField(max_length=50, verbose_name='Modelo')),
                ('categoria_veiculo', models.CharField(max_length=50, verbose_name='Categoria do Veículo')),
                ('fipe', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Valor FIPE')),
                ('tipo_documento', models.CharField(max_length=50, verbose_name='Tipo de Documento')),
                ('tipo_monta', models.CharField(max_length=50, verbose_name='Tipo de Monta')),
                ('tipo_chassi', models.CharField(max_length=50, verbose_name='Tipo de Chassi')),
                ('blindado', models.BooleanField(default=False, verbose_name='Blindado')),
                ('condicao', models.CharField(max_length=50, verbose_name='Condição')),
                ('condicao_funcionamento', models.CharField(max_length=50, verbose_name='Condição de Funcionamento')),
                ('numero_chassi', models.CharField(max_length=50, verbose_name='Número do Chassi')),
                ('chave', models.BooleanField(default=False, verbose_name='Possui Chave')),
                ('final_placa', models.CharField(max_length=1, verbose_name='Final da Placa')),
                ('combustivel', models.CharField(max_length=50, verbose_name='Combustível')),
                ('patio', models.CharField(max_length=100, verbose_name='Pátio')),
            ],
            options={
                'verbose_name': 'Veículo',
                'verbose_name_plural': 'Veículos',
            },
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('codigo_leilao', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='Código do Leilão')),
                ('descricao', models.TextField(verbose_name='Descrição do Leilão')),
                ('comitente', models.CharField(max_length=255, verbose_name='Comitente')),
                ('complemento', models.TextField(blank=True, null=True, verbose_name='Complemento')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data e Hora do Leilão')),
                ('duration_hours', models.PositiveIntegerField(default=2, verbose_name='Duração do Leilão (em horas)')),
                ('quantidade_lotes', models.PositiveIntegerField(default=0, verbose_name='Quantidade de Lotes')),
                ('thumbnail', models.ImageField(default='default/default_image.jpg', upload_to=auction_management.models.generate_auction_thumb_path)),
                ('documento_editais', models.FileField(blank=True, null=True, upload_to='editais/', verbose_name='Documento Edital (PDF)')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.auctioncategory', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Leilão',
                'verbose_name_plural': 'Leilões',
            },
        ),
    ]
