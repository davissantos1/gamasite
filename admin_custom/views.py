from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum 
from auction_management.models import RuralItem, RealEstate, Vehicle, OtherGoods, Auction, ItemImage
from payment.models import Bid, Payment
from django.utils.timezone import now
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist


@staff_member_required  # Garante que apenas usuários staff podem acessar
def admin_dashboard(request):
    # Contagem de itens
    items_count = RuralItem.objects.count() + RealEstate.objects.count() + Vehicle.objects.count() + OtherGoods.objects.count()

    # Contagem de lances, usuários, leilões
    users_count = User.objects.count()
    auctions_count = Auction.objects.filter(status='programado').count() + Auction.objects.filter(status='ao_vivo').count()
    bids_count = Bid.objects.count()

    # Valor total avaliado dos itens
    total_valor_avaliado = (
        RuralItem.objects.aggregate(Sum('valor_avaliado'))['valor_avaliado__sum'] or 0
    ) + (
        RealEstate.objects.aggregate(Sum('valor_avaliado'))['valor_avaliado__sum'] or 0
    ) + (
        Vehicle.objects.aggregate(Sum('valor_avaliado'))['valor_avaliado__sum'] or 0
    ) + (
        OtherGoods.objects.aggregate(Sum('valor_avaliado'))['valor_avaliado__sum'] or 0
    )

    # Passar os dados para o template
    context = {
        'users_count': users_count,
        'auctions_count': auctions_count,
        'items_count': items_count,
        'bids_count': bids_count,
        'total_valor_avaliado': total_valor_avaliado,
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def admin_ao_vivo(request):
    # Leilões programados
    leiloes_programados = Auction.objects.filter(status='programado')
    # Leilões ao vivo
    leiloes_ao_vivo = Auction.objects.filter(status='ao_vivo')
    
    return render(
        request,
        'admin/live_auctions.html',
        {
            'leiloes_programados': leiloes_programados,
            'leiloes_ao_vivo': leiloes_ao_vivo,
        }
    )

@staff_member_required
def gerenciar_ao_vivo(request, codigo_leilao):
    try:
        auction = Auction.objects.get(codigo_leilao=codigo_leilao)
    except Auction.DoesNotExist:
        return redirect('admin-ao-vivo')

    if auction.status not in ['programado', 'ao_vivo']:
        return redirect('admin-ao-vivo')

    if auction.status == 'programado':
        auction.status = 'ao_vivo'
        auction.ao_vivo_iniciado = True
        auction.date_time = now()
        auction.save()

    items = {
        'vehicles': auction.vehicles.all(),
        'real_estates': auction.real_estates.all(),
        'rural_items': auction.rural_items.all(),
        'other_goods': auction.other_goods.all(),
    }

    bids = {
        'vehicles': Bid.objects.filter(vehicle__in=items['vehicles'], is_valid=True).order_by('-amount'),
        'real_estates': Bid.objects.filter(real_estate__in=items['real_estates'], is_valid=True).order_by('-amount'),
        'rural_items': Bid.objects.filter(rural_item__in=items['rural_items'], is_valid=True).order_by('-amount'),
        'other_goods': Bid.objects.filter(other_goods__in=items['other_goods'], is_valid=True).order_by('-amount'),
    }

    highest_bids = {key: value.first() for key, value in bids.items()}

    ws_scheme = 'ws'
    port = settings.WS_PORT

    return render(request, 'admin/manage_live_auctions.html', {
        'auction': auction,
        'items': items,
        'bids': bids,
        'highest_bids': highest_bids,
        'ws_url': f'{ws_scheme}://{request.get_host().split(":")[0]}:{port}/ws/auction/{codigo_leilao}/',
    })

def set_current_item(request, item_id, item_type):
    """
    Define o item atual no leilão e envia uma mensagem via WebSocket para o frontend.
    :param item_id: ID do item.
    :param item_type: Tipo do item ('vehicle', 'realestate', 'ruralitem', 'othergoods').
    """
    try:
        # Determina o modelo do item com base no tipo passado
        if item_type == 'vehicle':
            item = Vehicle.objects.get(id=item_id)
        elif item_type == 'realestate':
            item = RealEstate.objects.get(id=item_id)
        elif item_type == 'ruralitem':
            item = RuralItem.objects.get(id=item_id)
        elif item_type == 'othergoods':
            item = OtherGoods.objects.get(id=item_id)
        else:
            return JsonResponse({"error": "Item não encontrado."}, status=400)

        auction = item.leilao  # Supondo que o leilão esteja relacionado ao item
        if auction.status != 'ao_vivo':  # Verifica se o leilão está ao vivo
            return JsonResponse({"error": "Leilão não está ao vivo."}, status=400)

        auction.current_item = item  # Define o item atual
        auction.save()

        # Enviar mensagem via WebSocket (em uma aplicação real, você pode usar um canal de websocket para enviar isso)
        # Vamos simular a comunicação WebSocket aqui com uma resposta JSON para o frontend
        return JsonResponse({"message": f"O item atual foi definido como: {item.nome}"})

    except ObjectDoesNotExist:
        return JsonResponse({"error": "Item não encontrado."}, status=404)


def set_winner_bid(request, item_id, item_type):
    """
    Define o lance vencedor para um item específico.
    :param item_id: ID do item.
    :param item_type: Tipo do item ('vehicle', 'realestate', 'ruralitem', 'othergoods').
    """
    # Determina o modelo do item com base no tipo passado
    item = None
    if item_type == 'vehicle':
        item = Vehicle.objects.get(id=item_id)
    elif item_type == 'realestate':
        item = RealEstate.objects.get(id=item_id)
    elif item_type == 'ruralitem':
        item = RuralItem.objects.get(id=item_id)
    elif item_type == 'othergoods':
        item = OtherGoods.objects.get(id=item_id)
    
    if not item:
        return redirect('admin-ao-vivo')  # Redireciona caso o item não seja encontrado

    auction = item.leilao  # Supondo que o leilão esteja relacionado ao item
    if auction.status != 'ao_vivo':  # Verifica se o leilão está ao vivo
        return redirect('admin-ao-vivo')  # Se não estiver ao vivo, redireciona

    # Busca o maior lance válido para o item
    highest_bid = Bid.objects.filter(item=item, is_valid=True).order_by('-amount').first()

    if highest_bid:
        item.lance_vencedor = highest_bid  # Atualiza o lance vencedor do item
        item.save()

    return redirect('admin:auction_management_auction_change', auction.id)

