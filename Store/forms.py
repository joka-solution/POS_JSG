from bootstrap3_datetime.widgets import DateTimePicker
from django.db import models
from dal import autocomplete
from django import forms
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from .models import control_almacen, inventario_global, cliente, control_venta, venta, inventario_store
from functools import partial
#from django.core.validators import validate_email
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DatePickerInput
#from multi_email_field.forms import MultiEmailField
#from bootstrap3_datepicker.fields import DatePickerField
#from bootstrap3_datepicker.widgets import DatePickerInput
#
class corte_select_userForm(forms.ModelForm):
    #registrado = forms.DateTimeField(widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options={'minuteStep': 1, 'format': 'yyyy-mm-dd hh:ii:ss ',}))
    #date = forms.DateField(widget=DatePickerInput())
    class Meta:
        model = control_venta
        fields = ['usuario', 'fecha_pago']
        widgets = {
            'fecha_pago': DatePickerInput(),
            #'fecha_pago': DatePickerInput(format='%Y-%m-%d'),
        }


class register_new_clientForm(forms.ModelForm):
    class Meta:
        model = cliente
        fields = ['nombre', 'apellido', 'direccion', 'email', 'Telefono', 'descripcion']

class Add_Article_inventory_Form(forms.ModelForm):
    contenido_pzas = forms.IntegerField(required=True, initial=1, disabled=False)
    class Meta:
        model = inventario_global
        fields = ['articulo_id', 'imagen', 'nombre', 'detalles', 'contenido_pzas', 'precio_venta', 'inventario']

class Add_Article_inventory_Store_Form(forms.ModelForm):
    contenido_pzas = forms.IntegerField(required=True, initial=1, disabled=False)
    class Meta:
        model = inventario_store
        fields = ['articulo_id', 'imagen', 'nombre', 'detalles', 'contenido_pzas', 'precio_venta', 'inventario']

class New_Venta_Form(forms.ModelForm):
    class Meta:
        model = control_venta
        fields = ['cliente']

class add_articles_Form(forms.ModelForm):
    articulo_id = forms.CharField(required=True, label='Ingresa un Articulo.', disabled=False)
    cantidad = forms.IntegerField(required=True, initial=1, disabled=False)
    class Meta:
        model = venta
        fields = ['articulo_id', 'cantidad']

class pago_con_Form(forms.ModelForm):
    pago_con = forms.CharField(required=False, label='Ingresa el monto total que esta recibiendo.', disabled=False)
    class Meta:
        model = control_venta
        fields = ['pago_con']

class a_cuenta_Form(forms.ModelForm):
    a_cuenta = forms.CharField(required=False, label='Ingrese el monto para realizar el apartado.', disabled=False)
    class Meta:
        model = control_venta
        fields = ['a_cuenta']

class imageForm(forms.ModelForm):
    class Meta:
        model = inventario_global
        fields = ['imagen', 'nombre', 'detalles', 'precio_venta', 'inventario']

class cargo_persona_Form(forms.ModelForm):
    class Meta:
        model = control_almacen
        fields = ['a_cargo']

class Contro_AlmacenForm(forms.ModelForm):
    #fecha = forms.DateTimeField(widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options={'minuteStep': 1, 'format': 'yyyy-mm-dd hh:ii:ss ',}))
    # initial_time = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    class Meta:
        model = control_almacen
        fields = ['articulo_id', 'nombre', 'movimiento', 'a_cargo', 'no_piezas']

    # def __init__(self, *args, **kwargs)
    #def setvalue(self):
     #   self.fields['nombre'].widget.attrs['disabled'] = 'disabled'
