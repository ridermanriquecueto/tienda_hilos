from django import forms
from .models import Producto
from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=255, required=True)
    ciudad = forms.CharField(max_length=100, required=True)
    codigo_postal = forms.CharField(max_length=10, required=True)
    comentarios = forms.CharField(widget=forms.Textarea, required=False)
    metodo_pago = forms.ChoiceField(choices=[('tarjeta', 'Tarjeta de crédito'), ('paypal', 'PayPal')], required=True)
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock','descripcion']
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre del producto'})
        self.fields['precio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Precio'})
        self.fields['stock'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Stock'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Descripción'})    


class CargaMasivaForm(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo CSV o Excel')

# forms.py


class CheckoutForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    direccion = forms.CharField(max_length=255, widget=forms.Textarea, label="Dirección")
    telefono = forms.CharField(max_length=15, label="Teléfono")
    metodo_pago = forms.ChoiceField(
        choices=[
            ('mercado_pago', 'Mercado Pago'),
            ('cuenta_dni', 'Cuenta DNI'),
            ('efectivo', 'Efectivo'),
            ('transferencia_bancaria', 'Transferencia Bancaria'),
            ('tarjeta_credito', 'Tarjeta de Crédito')
        ],
        label="Método de Pago"
    )
    metodo_envio = forms.ChoiceField(
        choices=[
            ('domicilio', 'Envío a Domicilio'),
            ('recoger_tienda', 'Recoger en Tienda')
        ],
        label="Método de Envío"
    )
    numero_tarjeta = forms.CharField(
        max_length=16,
        required=False,
        label="Número de Tarjeta",
        widget=forms.TextInput(attrs={'placeholder': 'Solo para tarjeta de crédito'})
    )
