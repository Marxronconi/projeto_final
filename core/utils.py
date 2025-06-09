from collections import Counter
import http.client
import ssl
from django.utils.timezone import localtime

def enviar_whatsapp_para_admin(pedido):
    conn = http.client.HTTPSConnection("api.ultramsg.com", context=ssl._create_unverified_context())

    token = "xygfcuzzlvmapdzy"
    instance_id = "124139"
    numero_destino = "5548996693674"

    # Agrupa produtos iguais por ID
    itens = pedido.itens.all()
    contador = Counter((item.produto.id, item.preco) for item in itens)

    lista = ""
    for (produto_id, preco), quantidade in contador.items():
        produto = next(item.produto for item in itens if item.produto.id == produto_id)
        lista += f"- {produto.nome} (x{quantidade}) - R$ {preco * quantidade:.2f}\n"

    total = pedido.total()
    horario = localtime(pedido.criado).strftime("%d/%m/%Y %H:%M")

    mensagem = (
        "------------TechRest------------\n"
        "📦 *Novo Pedido Recebido!*\n\n"
        f"🪑 *Mesa:* {pedido.mesa.numero}\n"
        f"🧾 *Itens do pedido:*\n{lista}\n\n"
        f"💰 *Total:* R$ {total:.2f}\n"
        f"⏰ *Horário:* {horario}\n\n"
        "Acesse o painel do gestor para mais detalhes."
    )

    payload = f"token={token}&to={numero_destino}&body={mensagem}"
    payload = payload.encode('utf8').decode('iso-8859-1')

    headers = {'content-type': "application/x-www-form-urlencoded"}
    conn.request("POST", f"/instance{instance_id}/messages/chat", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print("📨 Mensagem enviada:", data.decode("utf-8"))
