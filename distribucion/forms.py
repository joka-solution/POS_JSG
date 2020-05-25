from dal import autocomplete
from bootstrap3_datetime.widgets import DateTimePicker
from django.db import models
from django import forms
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from .models import inventario_distribucion, venta_distribucion
from functools import partial
#from django.core.validators import validate_email
from django.contrib.admin import widgets
from bootstrap_datepicker_plus import DatePickerInput
#from multi_email_field.forms import MultiEmailField
#from bootstrap3_datepicker.fields import DatePickerField
#from bootstrap3_datepicker.widgets import DatePickerInput



#


class Add_Article_inventory_Distr_Form(forms.ModelForm):
    contenido_pzas = forms.IntegerField(required=True, initial=12, disabled=False)
    class Meta:
        model = inventario_distribucion
        fields = ['nombre', 'inventario', 'imagen', 'detalles', 'contenido_pzas', 'precio_dist', 'precio_venta']

class add_articles_Form(forms.ModelForm):
    articulo_id = forms.CharField(required=True, label='Ingresa un Articulo.', disabled=False)
    cantidad = forms.IntegerField(required=True, initial=1, disabled=False)
    class Meta:
        model = venta_distribucion
        fields = ['articulo_id', 'cantidad']