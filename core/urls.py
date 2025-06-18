from django.urls import path
from . import views

urlpatterns = [
    # Página inicial e tablet
    path('', views.home, name='home'),
    path('tablet/', views.pagina_tablet, name='pagina_tablet'),
    path('categoria/<int:categoria_id>/', views.produtos_por_categoria, name='produtos_categoria'),

    # Mesa e segurança
    path('mesa/', views.escolher_mesa, name='escolher_mesa'),
    path('verificar-senha/', views.verificar_senha, name='verificar_senha'),

    # Carrinho (funciona tanto no tablet quanto no mobile)
    path('carrinho/', views.carrinho, name='carrinho_tablet'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('enviar-pedido/', views.enviar_pedido, name='enviar_pedido'),

    # Painel do gestor
    path('gestor/', views.gestor_pedidos, name='gestor_pedidos'),
    path('gestor/excluir/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
    path('gestor/status/<int:pedido_id>/', views.atualizar_status, name='atualizar_status'),

    # Ajax para categorias
    path('ajax/categoria/<int:id>/', views.carregar_produtos_categoria, name='carregar_produtos_categoria'),

    # Mobile
    path('mobile/', views.pagina_mobile, name='pagina_mobile'),
    path('mobile/categoria/<int:categoria_id>/', views.produtos_mobile, name='produtos_mobile'),
    path('mobile/carrinho/', views.carrinho_mobile, name='carrinho_mobile'),
    path('mobile/adicionar/<int:produto_id>/', views.adicionar_carrinho_mobile, name='adicionar_carrinho_mobile'),
    path('mobile/carrinho/remover/<int:produto_id>/', views.remover_carrinho_mobile, name='remover_carrinho_mobile'),
    path('mobile/escolher-mesa/', views.escolher_mesa_mobile, name='escolher_mesa_mobile'),
    path('mobile/enviar-pedido/', views.enviar_pedido_mobile, name='enviar_pedido_mobile'),
    path('pedido/<int:pedido_id>/pagar/', views.marcar_pedido_pago, name='marcar_pedido_pago'),

]
