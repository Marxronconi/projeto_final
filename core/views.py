from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Informacoes, Divulgacoes, Categoria, Produto, Mesa, Pedido, ItemPedido, Pedidos
from .utils import enviar_whatsapp_para_admin

def home(request):
    return redirect('/admin/')

def pagina_tablet(request):
    informacao = Informacoes.objects.filter(ativo=True).first()
    divulgacoes = Divulgacoes.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {
        'informacao': informacao,
        'divulgacoes': divulgacoes,
        'categorias': categorias
    })

def produtos_por_categoria(request, categoria_id):
    informacao = Informacoes.objects.filter(ativo=True).first()
    categoria = get_object_or_404(Categoria, id=categoria_id)
    produtos = Produto.objects.filter(categoria=categoria, ativo=True)
    categorias = Categoria.objects.all()
    return render(request, 'produtos_categoria.html', {
        'informacao': informacao,
        'categoria': categoria,
        'produtos': produtos,
        'categorias': categorias
    })

def escolher_mesa(request):
    if request.method == 'POST':
        mesa_id = request.POST.get('mesa_id')
        request.session['mesa_id'] = mesa_id
        return redirect('pagina_tablet')
    mesas = Mesa.objects.filter(ativo=True)
    return render(request, 'escolher_mesa.html', {'mesas': mesas})

def verificar_senha(request):
    destino = request.GET.get('next') or request.POST.get('next') or '/tablet'
    if request.method == 'POST':
        senha = request.POST.get('senha')
        if senha == 'techrest102030':
            return redirect(destino)
        else:
            messages.error(request, "Senha incorreta.")
    return render(request, 'verificar_senha.html', {'next': destino})

def adicionar_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho = request.session.get('carrinho', {})
        carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + 1
        request.session['carrinho'] = carrinho
    return redirect(request.META.get('HTTP_REFERER', '/tablet'))

def remover_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    if str(produto_id) in carrinho:
        if carrinho[str(produto_id)] > 1:
            carrinho[str(produto_id)] -= 1
        else:
            del carrinho[str(produto_id)]
        request.session['carrinho'] = carrinho
    return redirect('carrinho')

def carrinho(request):
    carrinho = request.session.get('carrinho', {})

    # se estiver como lista antiga, converte para dict com quantidade 1
    if isinstance(carrinho, list):
        carrinho = {str(produto_id): 1 for produto_id in carrinho}
        request.session['carrinho'] = carrinho
    produtos = []
    total = 0
    for produto_id, qtd in carrinho.items():
        produto = get_object_or_404(Produto, id=produto_id)
        subtotal = produto.preco * qtd
        total += subtotal
        produtos.append({
            'id': produto.id,
            'nome': produto.nome,
            'descricao': produto.descricao,
            'preco': produto.preco,
            'quantidade': qtd,
            'subtotal': subtotal
        })
    return render(request, 'carrinho.html', {
        'produtos': produtos,
        'total': total
    })

def enviar_pedido(request):
    mesa_id = request.session.get('mesa_id')
    if not mesa_id:
        return redirect('escolher_mesa')
    pedido = Pedidos.objects.create(mesa_id=mesa_id)
    carrinho = request.session.get('carrinho', {})
    for produto_id, qtd in carrinho.items():
        produto = Produto.objects.get(id=produto_id)
        for _ in range(qtd):
            ItemPedido.objects.create(pedido=pedido, produto=produto, preco=produto.preco)
    request.session['carrinho'] = {}
    enviar_whatsapp_para_admin(pedido)
    return redirect('pagina_tablet')

def gestor_pedidos(request):
    pedidos = Pedidos.objects.all().order_by('-criado')
    return render(request, 'gestor.html', {'pedidos': pedidos})

def excluir_pedido(request, pedido_id):
    pedido = Pedidos.objects.filter(id=pedido_id).first()
    if pedido:
        pedido.delete()
    return redirect('gestor_pedidos')

@require_POST
def atualizar_status(request, pedido_id):
    novo_status = request.POST.get('status')
    pedido = get_object_or_404(Pedidos, id=pedido_id)
    if novo_status in dict(Pedidos.STATUS_CHOICES).keys():
        pedido.status = novo_status
        pedido.save()
    return redirect('gestor_pedidos')

def carregar_produtos_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    produtos = Produto.objects.filter(categoria=categoria, ativo=True)
    html = render_to_string('partials/produtos_categoria.html', {
        'produtos': produtos,
        'categoria': categoria
    }, request=request)
    return JsonResponse({'html': html})