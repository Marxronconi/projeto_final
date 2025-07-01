import uuid
from django.db import models
from stdimage.models import StdImageField
from django.utils.timezone import now
from django.core.exceptions import ValidationError

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    pasta = instance.__class__.__name__.lower()
    return f'{pasta}/{filename}'

class Base(models.Model):
    criado = models.DateTimeField('Criação', auto_now_add=True)
    modificado = models.DateTimeField('Atualização', auto_now=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True

class Categoria(Base):
    nome = models.CharField('Nome', max_length=20)
    icone = models.CharField('Ícone', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = '1. Categorias'

    def __str__(self):
        return self.nome

class Produto(Base):
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2)
    descricao = models.TextField('Descrição', blank=True, null=True)
    categoria = models.ForeignKey('core.Categoria', verbose_name='Categoria', on_delete=models.DO_NOTHING)
    imagem = StdImageField(
        'Imagem',
        upload_to=get_file_path,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = '2. Produtos'

    def __str__(self):
        return self.nome

class Divulgacoes(Base):
    nome = models.CharField('Nome da Divulgação', max_length=100)
    imagem = StdImageField(
        'Imagem',
        upload_to=get_file_path,
        variations={'thumb': {'width': 1280, 'height': 720, 'crop': True}},
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Divulgação'
        verbose_name_plural = '3. Divulgações'

    def __str__(self):
        return self.nome

class Garcom(Base):
    nome = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Garçom'
        verbose_name_plural = '4. Garçons'

    def __str__(self):
        return self.nome

class Mesa(Base):
    numero = models.IntegerField('Número')
    garcom = models.ForeignKey('core.Garcom', verbose_name='Garçom', on_delete=models.DO_NOTHING)
    taxa = models.BooleanField('Taxa de serviço?', default=True)

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = '5. Mesas'

    def __str__(self):
        return f'Mesa {self.numero}'

class Informacoes(Base):
    nome = models.CharField('Nome do Restaurante', max_length=30)
    logo = StdImageField(
        'Logo',
        upload_to=get_file_path,
        variations={'thumb': {'width': 480, 'height': 480, 'crop': True}},
        blank=True,
        null=True
    )
    sobre = models.TextField('Sobre', max_length=1000, blank=True, null=True)
    TEMA_CHOICES = [
        ('claro', 'Claro'),
        ('escuro', 'Escuro'),
        ('amarelo', 'Amarelo'),
        ('vermelho', 'Vermelho'),
    ]

    tema = models.CharField('Tema do Cardápio', max_length=20, choices=TEMA_CHOICES, default='claro')

    def clean(self):
        if self.ativo:
            qs = Informacoes.objects.filter(ativo=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Já existe uma informação ativa. Desative antes de ativar outra.")

    class Meta:
        verbose_name = 'Informação️'
        verbose_name_plural = '6. Informações'

class Pedidos(Base):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparo', 'Em preparo'),
        ('finalizado', 'Finalizado'),
    ]

    mesa = models.ForeignKey('core.Mesa', verbose_name='Nº da Mesa', on_delete=models.DO_NOTHING)
    numero = models.IntegerField('Número do pedido', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    hora = models.TimeField(default=now)
    pago = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo = Pedidos.objects.order_by('-numero').first()
            self.numero = (ultimo.numero + 1) if ultimo and ultimo.numero else 1
        super().save(*args, **kwargs)

    def total(self):
        return sum(item.preco for item in self.itens.all())

    def __str__(self):
        return f"Pedido #{self.numero} - Mesa {self.mesa.numero}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('core.Produto', verbose_name='Produto', on_delete=models.CASCADE)
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if not self.preco:
            self.preco = self.produto.preco
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} (R$ {self.preco:.2f})"
