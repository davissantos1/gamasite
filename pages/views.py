# pages/views.py

from django.shortcuts import render, get_object_or_404
from categories.models import AuctionCategory
from auction_management.models import BaseItem, Auction
from django.utils.timezone import now
from calendar import Calendar
from django.contrib.auth.decorators import login_required
from auction_management.models import Auction, Vehicle, RealEstate, RuralItem, OtherGoods
from datetime import timedelta, datetime
from payment.models import Payment, Bid

def index(request):
    # Criar um dicionário para armazenar itens destacados por categoria
    itens_destacados = {
        'veiculos': [],
        'imoveis': [],
        'itens_rurais': [],
        'outros_bens': []
    }

    # Filtrar os itens destacados para cada tipo
    veiculos = Vehicle.objects.filter(destacado=True)[:3]
    imoveis = RealEstate.objects.filter(destacado=True)[:3]
    itens_rurais = RuralItem.objects.filter(destacado=True)[:3]
    outros_bens = OtherGoods.objects.filter(destacado=True)[:3]

    # Adicionar a categoria de cada item ao dicionário
    for veiculo in veiculos:
        veiculo.categoria = veiculo.leilao.categoria.nome  # A categoria vem do leilão
    for imovel in imoveis:
        imovel.categoria = imovel.leilao.categoria.nome
    for item_rural in itens_rurais:
        item_rural.categoria = item_rural.leilao.categoria.nome
    for item_bem in outros_bens:
        item_bem.categoria = item_bem.leilao.categoria.nome

    # Adicionar os itens ao dicionário com a categoria
    itens_destacados['veiculos'] = veiculos
    itens_destacados['imoveis'] = imoveis
    itens_destacados['itens_rurais'] = itens_rurais
    itens_destacados['outros_bens'] = outros_bens

    return render(request, 'pages/index.html', {'itens_destacados': itens_destacados})



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
                # Adicionar o nome do dia da semana abreviado
                week_data.append({'day': day, 'day_of_week': day.strftime('%a'), 'auctions': auctions})
        calendar_data.append(week_data)

    return render(request, 'pages/calendario.html', {'calendar': calendar_data})


def item_details(request, codigo_leilao, codigo_item):
    # Buscando o leilão
    leilao = get_object_or_404(Auction, codigo_leilao=codigo_leilao)

    # Tentando buscar o item baseado no tipo de item (Vehicle, RealEstate, RuralItem, OtherGoods)
    item = None
    item_type = None
    for model in [Vehicle, RealEstate, RuralItem, OtherGoods]:
        try:
            item = model.objects.get(codigo_item=codigo_item, leilao=leilao)
            item_type = model.__name__
            break
        except model.DoesNotExist:
            continue

    if not item:
        # Caso o item não seja encontrado
        return render(request, 'pages/item_not_found.html', {'codigo_item': codigo_item})

    # Certifique-se de que o item tem imagens associadas
    images = item.imagens.all() if item.imagens.exists() else []  # Obtenção das imagens associadas ao item

    # Passando o item encontrado para o template, incluindo as imagens
    return render(request, 'pages/item_details.html', {
        'leilao': leilao,
        'item': item,
        'item_type': item_type,
        'images': images,  # Passando as imagens associadas ao item
    })



def leilao_detalhe(request, id):
    leilao = get_object_or_404(Auction, codigo_leilao=id)
    return render(request, 'pages/leilao_detalhe.html', {'leilao': leilao})


@login_required
def inicio(request):
    return render(request, 'pages/dashboard/inicio.html')

@login_required
def lotes(request):
    return render(request, 'pages/dashboard/lotes.html')

@login_required
def lances(request):
    return render(request, 'pages/dashboard/lances.html')

@login_required
def financeiro_cliente(request):
    return render(request, 'pages/financeiro.html')

def live_auctions_view(request):
    current_time = now()

    # Leilões ao vivo
    live_auctions = Auction.objects.filter(
        date_time__lte=current_time,
        date_time__gte=current_time - timedelta(hours=1),
        active=True,
    )

    # Leilões programados para hoje
    start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    scheduled_auctions = Auction.objects.filter(
        date_time__gte=start_of_day,
        date_time__lt=end_of_day,
        active=True,
    )

    return render(request, 'live_auctions.html', {
        'live_auctions': live_auctions,
        'scheduled_auctions': scheduled_auctions,
    })



def financeiro(request):
    pagamentos_pendentes = Payment.objects.filter(status='pendente')
    pagamentos_realizados = Payment.objects.filter(status='pago')

    context = {
        'pagamentos_pendentes': pagamentos_pendentes,
        'pagamentos_realizados': pagamentos_realizados,
    }
    return render(request, 'financeiro/financeiro.html', context)
