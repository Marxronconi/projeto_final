from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tablet/', views.pagina_tablet, name='pagina_tablet'),
    path('categoria/<int:categoria_id>/', views.produtos_por_categoria, name='produtos_categoria'),
    path('mesa/', views.escolher_mesa, name='escolher_mesa'),
    path('verificar-senha/', views.verificar_senha, name='verificar_senha'),

    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('enviar-pedido/', views.enviar_pedido, name='enviar_pedido'),

    path('gestor/', views.gestor_pedidos, name='gestor_pedidos'),
    path('gestor/excluir/<int:pedido_id>/', views.excluir_pedido, name='excluir_pedido'),
    path('gestor/status/<int:pedido_id>/', views.atualizar_status, name='atualizar_status'),

    path('ajax/categoria/<int:id>/', views.carregar_produtos_categoria, name='carregar_produtos_categoria'),

]
