from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from auction_management.models import RuralItem, RealEstate, Vehicle, OtherGoods, Auction, BaseItem
from payment.models import Bid, Payment


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
