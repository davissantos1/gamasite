from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from auction_management.models import Auction
from auction_management.models import BaseItem


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
    # Substitua pelos dados reais do contexto
    context = {
        'users_count': 10,  # Exemplo
        'auctions_count': 5,
        'categories_count': 3,
        'bids_count': 20,
    }
    return render(request, 'admin/dashboard.html', context)
