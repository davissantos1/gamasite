# pages/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from calendar import Calendar
from django.contrib.auth.decorators import login_required
from auction_management.models import Auction, Vehicle, RealEstate, RuralItem, OtherGoods, ItemImage
from datetime import timedelta, datetime
from payment.models import Payment, Bid
from django.contrib import messages
from django.utils.timezone import localtime
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.conf import settings

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
                # Filtrar leilões do dia com status 'programado' ou 'ao_vivo'
                auctions = Auction.objects.filter(
                    date_time__date=day,
                    status__in=['programado', 'ao_vivo']
                ).order_by('date_time')
                # Adicionar o nome do dia da semana abreviado
                week_data.append({'day': day, 'day_of_week': day.strftime('%a'), 'auctions': auctions})
        calendar_data.append(week_data)

    return render(request, 'pages/calendario.html', {'calendar': calendar_data})


def item_details(request, codigo_leilao, codigo_item):
    # Buscando o leilão
    leilao = get_object_or_404(Auction, codigo_leilao=codigo_leilao)

    # Ajustar a data para o fuso horário local
    leilao_data = localtime(leilao.date_time)

    # Tentando buscar o item baseado no tipo de item (Vehicle, RealEstate, RuralItem, OtherGoods)
    item = None
    item_type = None
    images = []

    for model in [Vehicle, RealEstate, RuralItem, OtherGoods]:
        try:
            item = model.objects.get(codigo_item=codigo_item, leilao=leilao)
            item_type = model.__name__

            # Buscar imagens associadas ao item
            if item_type == 'Vehicle':
                images = ItemImage.objects.filter(vehicle=item)
            elif item_type == 'RealEstate':
                images = ItemImage.objects.filter(real_estate=item)
            elif item_type == 'RuralItem':
                images = ItemImage.objects.filter(rural_item=item)
            elif item_type == 'OtherGoods':
                images = ItemImage.objects.filter(other_goods=item)

            break
        except model.DoesNotExist:
            continue

    if not item:
        # Caso o item não seja encontrado
        return render(request, 'pages/item_not_found.html', {'codigo_item': codigo_item})

    # Buscar lances associados ao item
    bids = Bid.objects.filter(
        real_estate=item if item_type == 'RealEstate' else None,
        vehicle=item if item_type == 'Vehicle' else None,
        rural_item=item if item_type == 'RuralItem' else None,
        other_goods=item if item_type == 'OtherGoods' else None,
        is_valid=True  # Apenas lances válidos
    ).order_by('-amount')  # Ordena pelos maiores lances

    # Obter o maior lance (se houver)
    highest_bid = bids.first() if bids.exists() else None

    # Passando o item, imagens, lances e o maior lance para o template
    return render(request, 'pages/item_details.html', {
        'leilao': leilao,
        'item': item,
        'item_type': item_type,
        'images': images,
        'bids': bids,  # Passa os lances para o template
        'highest_bid': highest_bid,  # Passa o maior lance
        'leilao_data': leilao_data,  # Passa a data do leilão ajustada para o template
    })

def leilao_detalhe(request, codigo_leilao):
    leilao = get_object_or_404(Auction, codigo_leilao=codigo_leilao)  # Usar codigo_leilao
    return render(request, 'pages/leilao_detalhe.html', {'leilao': leilao, 'now': timezone.now()})

def ao_vivo(request, codigo_leilao):
    # Obtém o leilão com o código especificado
    auction = get_object_or_404(Auction, codigo_leilao=codigo_leilao)
    
    # Verifica se o status do leilão é "ao_vivo"
    if auction.status != 'ao_vivo':
        return HttpResponseForbidden("O leilão não está ao vivo no momento.")

    # Busca todos os itens associados ao leilão
    vehicles = Vehicle.objects.filter(leilao=auction)
    real_estates = RealEstate.objects.filter(leilao=auction)
    rural_items = RuralItem.objects.filter(leilao=auction)
    other_goods = OtherGoods.objects.filter(leilao=auction)

    # Configurar o esquema e a porta manualmente
    ws_scheme = 'ws'

    port = settings.WS_PORT

    # Se for produção e usando HTTPS, ajuste para wss
    # if request.is_secure():
    #   ws_scheme = 'wss'
    #   port = '443'

    # Contexto para o template
    context = {
        'auction': auction,
        'vehicles': vehicles,
        'real_estates': real_estates,
        'rural_items': rural_items,
        'other_goods': other_goods,
        'ws_url': f'{ws_scheme}://{request.get_host().split(":")[0]}:{port}/ws/auction/{codigo_leilao}/'
    }

    # Renderiza a página ao vivo com todos os itens
    return render(request, 'pages/ao_vivo.html', context)


@login_required
def inicio(request):
    # Busca todos os lances do usuário, incluindo as relações necessárias
    lances_usuario = Bid.objects.filter(user=request.user).select_related(
        'real_estate', 'vehicle', 'rural_item', 'other_goods'
    )

    lotes = []
    lances_detalhados = []  # Lista para armazenar os lances detalhados

    for lance in lances_usuario:
        item = None
        tipo_item = None

        # Verifica o tipo do item e atribui
        if lance.real_estate:
            item = lance.real_estate
            tipo_item = 'Imóvel'
        elif lance.vehicle:
            item = lance.vehicle
            tipo_item = 'Veículo'
        elif lance.rural_item:
            item = lance.rural_item
            tipo_item = 'Item Rural'
        elif lance.other_goods:
            item = lance.other_goods
            tipo_item = 'Outros Bens'

        if item:
            lote = {
                'item': item,
                'tipo': tipo_item,
                'valor_lance': lance.amount,
                'data': lance.timestamp,
                'imagem': getattr(item, 'thumbnail', None), 
            }
            lotes.append(lote)

            # Adiciona o lance detalhado à lista
            maior_lance = Bid.get_highest_bid(item)  # Obtém o maior lance associado ao item
            lance_detalhado = {
                'tipo': tipo_item,
                'item_nome': item.nome if hasattr(item, 'nome') else str(item),
                'valor_lance': lance.amount,
                'data_lance': lance.timestamp,
                'is_valid': lance.is_valid,  # Validade do lance
                'maior_lance': maior_lance.amount if maior_lance else None  # Maior lance
            }
            lances_detalhados.append(lance_detalhado)

    # Coletar os IDs dos leilões associados aos lotes
    leiloes_ids = set(lote['item'].leilao.codigo_leilao for lote in lotes if hasattr(lote['item'], 'leilao'))

    # Buscar os leilões com os IDs coletados
    leiloes = Auction.objects.filter(codigo_leilao__in=leiloes_ids)

    # Contexto para o template
    context = {
        'lances': lances_detalhados,  # Passa a lista detalhada dos lances
        'lotes': lotes,  # Dados detalhados dos lotes
        'leiloes': leiloes,  # Dados dos leilões associados
    }

    return render(request, 'pages/dashboard/inicio.html', context)



@login_required
def lotes(request):
    # Obter lances do usuário atual
    lances_usuario = Bid.objects.filter(user=request.user).select_related(
        'real_estate', 'vehicle', 'rural_item', 'other_goods'
    )
    
    # Criar uma lista com os itens baseados nos lances
    lotes = []
    for lance in lances_usuario:
        if lance.real_estate:
            lotes.append({'item': lance.real_estate, 'tipo': 'Imóvel', 'valor_lance': lance.amount, 'data': lance.timestamp})
        elif lance.vehicle:
            lotes.append({'item': lance.vehicle, 'tipo': 'Veículo', 'valor_lance': lance.amount, 'data': lance.timestamp})
        elif lance.rural_item:
            lotes.append({'item': lance.rural_item, 'tipo': 'Item Rural', 'valor_lance': lance.amount, 'data': lance.timestamp})
        elif lance.other_goods:
            lotes.append({'item': lance.other_goods, 'tipo': 'Outros Bens', 'valor_lance': lance.amount, 'data': lance.timestamp})
    
    # Passar dados para o template
    return render(request, 'pages/dashboard/lotes.html', {'lotes': lotes})


@login_required
def lances(request):
    lances_usuario = Bid.objects.filter(user=request.user).select_related(
        'real_estate', 'vehicle', 'rural_item', 'other_goods'
    )
    return render(request, 'pages/dashboard/lances.html', {'lances': lances_usuario})


@login_required
def financeiro_cliente(request):
    return render(request, 'pages/financeiro.html')

def leiloes_ao_vivo(request):
    current_time = now()

    # Leilões ao vivo (status 'ao_vivo')
    live_auctions = Auction.objects.filter(
        status='ao_vivo',
        date_time__lte=current_time,
        date_time__gte=current_time - timedelta(hours=1)
    )

    # Leilões programados para hoje (status 'programado')
    start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    scheduled_auctions = Auction.objects.filter(
        status='programado',
        date_time__gte=start_of_day,
        date_time__lt=end_of_day
    )

    return render(request, 'pages/leiloes_ao_vivo.html', {
        'live_auctions': live_auctions,
        'scheduled_auctions': scheduled_auctions,
    })


@login_required
def create_bid(request, codigo_leilao, codigo_item):
    if request.method == "POST":
        valor_lance = request.POST.get("valor_lance")
        try:
            valor_lance = float(valor_lance)
        except ValueError:
            messages.error(request, "O valor do lance deve ser numérico.")
            return redirect('pages:item_details', codigo_leilao=codigo_leilao, codigo_item=codigo_item)

        # Buscar o arrematante
        arrematante = request.user.arrematante

        # Verificar se o arrematante pode dar lances
        if not arrematante.pode_dar_lance:
            messages.error(request, "Você não pode dar lances até enviar todos os documentos necessários.")
            return redirect('pages:item_details', codigo_leilao=codigo_leilao, codigo_item=codigo_item)

        # Buscar o leilão
        leilao = get_object_or_404(Auction, codigo_leilao=codigo_leilao)

        # Buscar o item associado ao leilão
        item = (
            Vehicle.objects.filter(codigo_item=codigo_item, leilao=leilao).first() or
            RealEstate.objects.filter(codigo_item=codigo_item, leilao=leilao).first() or
            RuralItem.objects.filter(codigo_item=codigo_item, leilao=leilao).first() or
            OtherGoods.objects.filter(codigo_item=codigo_item, leilao=leilao).first()
        )

        if not item:
            messages.error(request, "Item não encontrado.")
            return redirect('pages:leiloes_ao_vivo')

        # Verificar valor inicial
        if valor_lance < item.valor_inicial:
            messages.error(request, f"O lance deve ser maior ou igual a R$ {item.valor_inicial:.2f}.")
            return redirect('pages:item_details', codigo_leilao=codigo_leilao, codigo_item=codigo_item)

        # Criar o lance
        Bid.objects.create(
            user=request.user,
            amount=valor_lance,
            real_estate=item if isinstance(item, RealEstate) else None,
            vehicle=item if isinstance(item, Vehicle) else None,
            rural_item=item if isinstance(item, RuralItem) else None,
            other_goods=item if isinstance(item, OtherGoods) else None
        )

        messages.success(request, "Lance realizado com sucesso!")
        return redirect('pages:item_details', codigo_leilao=codigo_leilao, codigo_item=codigo_item)

    messages.error(request, "Método inválido.")
    return redirect('pages:home')



def financeiro(request):
    pagamentos_pendentes = Payment.objects.filter(status='pendente')
    pagamentos_realizados = Payment.objects.filter(status='pago')

    context = {
        'pagamentos_pendentes': pagamentos_pendentes,
        'pagamentos_realizados': pagamentos_realizados,
    }
    return render(request, 'financeiro/financeiro.html', context)
