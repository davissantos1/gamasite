from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from auction_management.models import Auction, BaseItem, Bid
from django.db.models import Sum, Count

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
    # Calcula o número total de itens cadastrados
    items_count = BaseItem.objects.count()

    # Calcula o valor total avaliado dos itens acumulados
    total_valor_avaliado = BaseItem.objects.aggregate(Sum('valor_avaliado'))['valor_avaliado__sum'] or 0

    # Número de usuários (Exemplo, pode ser modificado)
    users_count = User.objects.count()

    # Número de leilões ativos (Você pode adicionar a lógica do seu modelo de leilão)
    auctions_count = Auction.objects.filter(active=True).count()

    # Número de lances recebidos
    bids_count = Bid.objects.count()  # Assumindo que você tem um modelo Bid

    context = {
        'users_count': users_count,
        'auctions_count': auctions_count,
        'items_count': items_count,
        'bids_count': bids_count,
        'total_valor_avaliado': total_valor_avaliado,
    }

    return render(request, 'admin/dashboard.html', context)