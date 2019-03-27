from django.forms import ModelForm
from .models import Destinatario, Endereco

class DestinatarioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DestinatarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Destinatario
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']


class EnderecoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnderecoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'cidade', 'cep', 'estado']