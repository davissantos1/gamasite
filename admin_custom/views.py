from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum 
from auction_management.models import RuralItem, RealEstate, Vehicle, OtherGoods, Auction, ItemImage
from payment.models import Bid, Payment


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
    # Recupera o leilão que foi iniciado
    try:
        auction = Auction.objects.get(codigo_leilao=codigo_leilao)
    except Auction.DoesNotExist:
        return redirect('admin-ao-vivo')  # Redireciona se o leilão não existir

    # Verifica se o status do leilão permite acesso a esta página
    if auction.status not in ['programado', 'ao_vivo']:
        return redirect('admin-ao-vivo')

    # Se o leilão estiver programado, muda o status para "ao_vivo"
    if auction.status == 'programado':
        auction.status = 'ao_vivo'
        auction.ao_vivo_iniciado = True
        auction.save()
        

    # Recupera os itens associados ao leilão
    items = {
        'vehicles': auction.vehicles.all(),
        'real_estates': auction.real_estates.all(),
        'rural_items': auction.rural_items.all(),
        'other_goods': auction.other_goods.all(),
    }

    # Adiciona os lances para cada tipo de item
    bids = {
        'vehicles': Bid.objects.filter(vehicle__in=items['vehicles'], is_valid=True).order_by('-amount'),
        'real_estates': Bid.objects.filter(real_estate__in=items['real_estates'], is_valid=True).order_by('-amount'),
        'rural_items': Bid.objects.filter(rural_item__in=items['rural_items'], is_valid=True).order_by('-amount'),
        'other_goods': Bid.objects.filter(other_goods__in=items['other_goods'], is_valid=True).order_by('-amount'),
    }

    # Determina o maior lance por tipo de item
    highest_bids = {key: value.first() for key, value in bids.items()}

    # Renderiza o template com os dados necessários
    return render(request, 'admin/manage_live_auctions.html', {
        'auction': auction,
        'items': items,
        'bids': bids,
        'highest_bids': highest_bids,
    })



