from django.forms import ModelForm
from .models import Etiqueta

class EtiqForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EtiqForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control col-sm-6'
    class Meta:
        model = Etiqueta
        fields = ['nome', 'funcao', 'email', 'orgao', 'endereco']
