import json
from channels.generic.websocket import AsyncWebsocketConsumer
from auction_management.models import Auction, Vehicle, RealEstate, RuralItem, OtherGoods
from payment.models import Bid  

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Estabelecer conexão WebSocket
        self.group_name = "auction_group"  # Aqui você pode usar o id do leilão ou algo único
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Obter o leilão e o item atual
        auction = await Auction.objects.get(codigo_leilao=self.scope['url_route']['kwargs']['auction_id'])
        current_item = auction.current_item

        # Enviar dados do item atual
        await self.send(text_data=json.dumps({
            'action': 'get_item_data',
            'item': {
                'nome': current_item.nome,
                'tipo': current_item.tipo,
                'thumbnail_url': current_item.thumbnail.url,
                'descricao': current_item.descricao,
                'valor_inicial': str(current_item.valor_inicial),  # Formatação para enviar como string
            },
            'bids': [
                {'usuario': bid.usuario.username, 'valor': str(bid.valor)}
                for bid in current_item.bids.all()
            ]
        }))

    async def disconnect(self, close_code):
        # Fechar o WebSocket
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'place_bid':
            bid_value = data.get('bid_value')
            # Aqui você pode processar o lance, salvar no banco de dados, etc.
            print(f"Lance recebido: R$ {bid_value}")

            # Depois de processar o lance, enviar a atualização para todos os usuários
            # Aqui você pode pegar os dados atualizados, como o novo valor dos lances
            # e enviar para os clientes
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'auction_message',
                    'item': {
                        'nome': 'Novo Item',  # Atualize com dados reais
                        'tipo': 'Novo Tipo',
                        'thumbnail_url': 'novo_url_imagem',  # Atualize com a URL do item
                        'descricao': 'Nova Descrição',
                        'valor_inicial': '2000',  # Atualize o valor
                    },
                    'bids': [
                        {'usuario': 'Usuario Atualizado', 'valor': '1500'}  # Atualize com novos lances
                    ]
                }
            )

    async def auction_message(self, event):
        # Enviar mensagem para o WebSocket
        await self.send(text_data=json.dumps({
            'item': event['item'],
            'bids': event['bids']
        }))


    async def send_initial_data(self):
        auction = await self.get_auction()
        items = await self.get_items(auction)
        bids = await self.get_bids(items)

        print('Sending initial data:', items, bids)  # Adicione esse print para depuração
        
        if items:
            first_item = items[0]
            item_bids = bids[0] if bids else []
            first_item_data = {
                'item': {
                    'nome': first_item['nome'],
                    'tipo': first_item['tipo'],
                    'thumbnail_url': first_item['thumbnail_url'],
                    'descricao': first_item['descricao'],
                    'valor_inicial': first_item['valor_inicial'],
                },
                'bids': [
                    {'usuario': bid.usuario.username, 'valor': bid.valor}
                    for bid in item_bids
                ]
            }
            await self.send(text_data=json.dumps(first_item_data))

    async def send_item_data(self):
        # Obtém o leilão e o item atual
        auction = await self.get_auction()
        item = auction.current_item
        bids = await self.get_bids([item])

        # Ordena os lances do maior para o menor e limita a 5 primeiros
        sorted_bids = sorted(bids, key=lambda bid: bid.valor, reverse=True)[:5]

        item_data = {
            'item': {
                'nome': item.nome,
                'tipo': item.tipo,
                'thumbnail_url': item.thumbnail.url,
                'descricao': item.descricao,
                'valor_inicial': item.valor_inicial,
            },
            'bids': [
                {'usuario': bid.usuario.username, 'valor': bid.valor}
                for bid in sorted_bids
            ]
        }

        await self.send(text_data=json.dumps(item_data))


    async def place_bid(self, bid_value):
        # Registra o lance feito pelo cliente
        auction = await self.get_auction()
        item = auction.vehicles.first()  # Aqui, use o item atual
        bid = Bid.objects.create(vehicle=item, valor=bid_value)

        # Atualiza os lances
        bids = await self.get_bids([item])

        # Envia os dados do lance
        bid_data = {
            'bids': [
                {'usuario': bid.usuario.username, 'valor': bid.valor}
                for bid in bids
            ]
        }

        await self.send(text_data=json.dumps(bid_data))

    async def next_item(self):
        # Muda para o próximo item
        auction = await self.get_auction()
        next_item = auction.vehicles.all().first()  # Ajuste para o próximo item
        await self.send_item_data()

    async def get_auction(self):
        return await Auction.objects.get(codigo_leilao=self.auction_id)

    async def get_items(self, auction):
        items = []

        # Adiciona veículos, se existirem
        for vehicle in auction.vehicles.all():
            items.append({
                'nome': vehicle.nome,
                'tipo': 'Veículo',
                'thumbnail_url': vehicle.thumbnail.url,
                'descricao': vehicle.descricao,
                'valor_inicial': vehicle.valor_inicial
            })

        # Adiciona imóveis, se existirem
        for real_estate in auction.real_estates.all():
            items.append({
                'nome': real_estate.nome,
                'tipo': 'Imóvel',
                'thumbnail_url': real_estate.thumbnail.url,
                'descricao': real_estate.descricao,
                'valor_inicial': real_estate.valor_inicial
            })

        # Adiciona itens rurais, se existirem
        for rural_item in auction.rural_items.all():
            items.append({
                'nome': rural_item.nome,
                'tipo': 'Rural',
                'thumbnail_url': rural_item.thumbnail.url,
                'descricao': rural_item.descricao,
                'valor_inicial': rural_item.valor_inicial
            })

        # Adiciona outros bens, se existirem
        for other_good in auction.other_goods.all():
            items.append({
                'nome': other_good.nome,
                'tipo': 'Outros Bens',
                'thumbnail_url': other_good.thumbnail.url,
                'descricao': other_good.descricao,
                'valor_inicial': other_good.valor_inicial
            })

        # Se não houver itens de nenhum tipo, pode retornar uma lista vazia ou uma mensagem
        if not items:
            items = [{'tipo': 'Nenhum item disponível', 'nome': 'Nenhum item', 'descricao': 'Não há itens disponíveis para o leilão no momento.'}]
        
        return items

    async def get_bids(self, items):
        bids = []
        for item in items:
            if isinstance(item, Vehicle):
                bids.append(Bid.objects.filter(vehicle=item).order_by('-valor').first())
            elif isinstance(item, RealEstate):
                bids.append(Bid.objects.filter(real_estate=item).order_by('-valor').first())
            elif isinstance(item, RuralItem):
                bids.append(Bid.objects.filter(rural_item=item).order_by('-valor').first())
            elif isinstance(item, OtherGoods):
                bids.append(Bid.objects.filter(other_goods=item).order_by('-valor').first())
        return bids
