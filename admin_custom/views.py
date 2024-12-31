from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum 
from auction_management.models import RuralItem, RealEstate, Vehicle, OtherGoods, Auction
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
    # Apenas leilões com status 'programado' para serem iniciados
    leiloes_programados = Auction.objects.filter(status='programado')
    return render(request, 'admin/live_auctions.html', {'leiloes_programados': leiloes_programados})

@staff_member_required
def iniciar_ao_vivo(request, codigo_leilao):
    # Recupera o leilão que foi iniciado
    auction = Auction.objects.get(codigo_leilao=codigo_leilao)

    # Se o leilão não está programado ou já foi finalizado, redireciona
    if auction.status not in ['programado', 'ao_vivo']:
        return redirect('admin-ao-vivo')

    # Inicia o leilão ao vivo e muda seu status
    auction.status = 'ao_vivo'
    auction.ao_vivo_iniciado = True
    auction.save()

    # Aqui você pode adicionar lógica para passar os itens do leilão, definir vencedor, etc.

    return render(request, 'admin/begin_live_auctions.html', {'auction': auction})

@staff_member_required
def finalizar_leilao(request, codigo_leilao):
    auction = Auction.objects.get(codigo_leilao=codigo_leilao)
    auction.status = 'finalizado'
    auction.save()
    return redirect('admin-ao-vivo')

@staff_member_required
def proximo_item_leilao(request, codigo_leilao):
    auction = Auction.objects.get(codigo_leilao=codigo_leilao)
    # Lógica para determinar o próximo item
    next_item = auction.vehicles.all().first()  # Exemplo de lógica simples, pode ser mais complexa
    return render(request, 'admin/begin_live_auctions.html', {'auction': auction, 'current_item': next_item})


