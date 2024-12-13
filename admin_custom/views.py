from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from auction_management.models import RuralItem, RealEstate, Vehicle, OtherGoods, Auction, Bid, BaseItem

@login_required
def list_clients(request):
    clients = User.objects.all().order_by('date_joined')
    return render(request, 'admin/client_list.html', {'clients': clients})


@login_required
def list_auctions(request):
    # Ordenando pelos campos corretos, neste caso 'codigo_leilao'
    auctions = Auction.objects.all().order_by('codigo_leilao')
    return render(request, 'admin/auction_list.html', {'auctions': auctions})


@login_required
def list_items(request):
    items = BaseItem.objects.all().order_by('codigo_item')
    return render(request, 'admin/item_list.html', {'items': items})



@staff_member_required  # Garante que apenas usuários staff podem acessar
def admin_dashboard(request):
    # Contagem de itens
    items_count = RuralItem.objects.count() + RealEstate.objects.count() + Vehicle.objects.count() + OtherGoods.objects.count()

    # Contagem de lances, usuários, leilões
    users_count = User.objects.count()
    auctions_count = Auction.objects.filter(active=True).count()
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
