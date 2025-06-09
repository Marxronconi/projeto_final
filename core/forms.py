import os
from django import forms
from django.conf import settings
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icones_dir = os.path.join(settings.BASE_DIR, 'core', 'static', 'icons')

        try:
            arquivos = os.listdir(icones_dir)
        except FileNotFoundError:
            arquivos = []

        escolhas = [(f, f) for f in arquivos if f.endswith('.png')]
        self.fields['icone'] = forms.ChoiceField(choices=escolhas, label='Ícone')

    class Meta:
        model = Categoria
        fields = '__all__'
