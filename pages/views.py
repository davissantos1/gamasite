# pages/views.py

from django.shortcuts import render, get_object_or_404
from categories.models import AuctionCategory
from auction_management.models import BaseItem, Auction
from django.utils.timezone import now
from calendar import Calendar
from datetime import date


def index(request):
    categories = AuctionCategory.objects.prefetch_related('featured_item').all()
    return render(request, 'pages/index.html', {'categories': categories})

def como_participar(request):
    return render(request, 'pages/como_participar.html')

def leiloes_ao_vivo(request):
    leiloes = Auction.objects.filter(active=True)
    return render(request, 'pages/leiloes_ao_vivo.html', {'leiloes': leiloes})

def calendario(request):
    # Obter o mês e ano atual
    today = now().date()
    calendar = Calendar()
    days_of_month = calendar.monthdatescalendar(today.year, today.month)

    # Criar estrutura de dados para o calendário
    calendar_data = []
    for week in days_of_month:
        week_data = []
        for day in week:
            # Dias fora do mês atual são ignorados
            if day.month != today.month:
                week_data.append(None)
            else:
                # Filtrar leilões do dia
                auctions = Auction.objects.filter(date_time__date=day, active=True).order_by('date_time')
                week_data.append({'day': day, 'auctions': auctions})
        calendar_data.append(week_data)

    return render(request, 'pages/calendario.html', {'calendar': calendar_data})


def item_detail(request, id):
    # Recupera o item pelo ID ou retorna 404
    item = get_object_or_404(BaseItem, id=id)
    return render(request, 'pages/item_detail.html', {'item': item})