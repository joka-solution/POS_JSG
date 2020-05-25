from __future__ import unicode_literals
from django.conf import settings
from django.urls import reverse
from django.db import models

from usuario.models import User


# Create your models here.

venta_status = (
    ('Abierta', 'Abierta'),
    ('Pendiente', 'Pendiente'),
    ('Apartado', 'Apartado'),
    ('Cancelada', 'Cancelada'),
    ('Cerrada', 'Cerrada'),
    ('Concesion', 'Concesion'),
    ('Liquidado', 'Liquidado'),
)

movimiento_almacen = (
    ('Entrada', 'Entrada'),
    ('Traspaso', 'Traspaso'),
    ('Salida', 'Salida'),
)

class cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=99999999, blank=False, null=False)
    apellido = models.CharField(max_length=99999999, blank=True, null=True)
    direccion = models.CharField(max_length=99999999, blank=False, null=False)
    email = models.EmailField(null=True, blank=True)
    Telefono = models.IntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=99999999, blank=True, null=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" % (self.id)

    def __str__(self):
        return "%s" % (self.nombre)

    def get_cliente_url(self):
        return reverse("Store:clientedetalleview", kwargs={"pk":self.pk})

class inventario_global(models.Model):
    id = models.AutoField(primary_key=True)
    articulo_id = models.CharField(max_length=99999999, blank=False, null=False, unique=True)
    imagen = models.ImageField(upload_to = 'Articulos/', blank=True, null=True)
    barcode = models.ImageField(upload_to = 'BarCode/', blank=True, null=True)
    nombre = models.CharField(max_length=99999999, blank=False, null=False)
    detalles = models.CharField(max_length=99999999, blank=True, null=True)
    contenido_pzas = models.CharField(max_length=99999999, blank=True, null=False)
    #PRECIOS
    precio_compra = models.CharField(max_length=99999999, blank=True, null=False)
    precio_distribucion = models.CharField(max_length=99999999, blank=True, null=True)
    precio_venta = models.IntegerField(null=True, blank=True)
    #INVENTARIOS ALMACEN GLOBAL
    inventario = models.IntegerField(null=True, blank=True)
    #existencia = models.IntegerField(null=True, blank=True)
    #MONTOS GLOBALES
    inversion = models.CharField(max_length=99999999, blank=True, null=False)
    monto_total = models.CharField(max_length=99999999, blank=True, null=False)

    unidades_vendidas = models.CharField(max_length=99999999, null=True, blank=True)

    numero_caja = models.CharField(max_length=99999999, null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.imagen)

    def __str__(self):
        return "%s" %(self.articulo_id)

    def get_edit_url(self):
        return reverse("Store:editimage", kwargs={"pk":self.pk})

    def control_inventory_url(self):
        return reverse("Store:add_or_remove_inventory", kwargs={"pk":self.pk})

class inventario_store(models.Model):
    id = models.AutoField(primary_key=True)
    articulo_id = models.CharField(max_length=99999999, blank=False, null=False, unique=True)
    imagen = models.ImageField(upload_to = 'Articulos/', blank=True, null=True)
    barcode = models.ImageField(upload_to = 'BarCode/', blank=True, null=True)
    nombre = models.CharField(max_length=99999999, blank=False, null=False)
    detalles = models.CharField(max_length=99999999, blank=True, null=True)
    contenido_pzas = models.CharField(max_length=99999999, blank=True, null=False)
    #PRECIOS
    precio_venta = models.IntegerField(null=True, blank=True)
    #INVENTARIOS ALMACEN GLOBAL
    inventario = models.IntegerField(null=True, blank=True)
    unidades_vendidas = models.IntegerField(null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.imagen)

    def __str__(self):
        return "%s" %(self.articulo_id)

class empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=999999, blank=False, null=False)
    direccion = models.CharField(max_length=999999, blank=False, null=False)
    telefono = models.CharField(max_length=9999, blank=True, null=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" % (self.nombre)

    def __str__(self):
        return "%s" % (self.nombre)

class control_almacen(models.Model):
    id = models.AutoField(primary_key=True)
    articulo_id = models.CharField(max_length=99999999, blank=False, null=False)
    nombre = models.CharField(max_length=99999999, blank=False, null=False)
    movimiento = models.CharField(max_length=99999999, choices=movimiento_almacen, blank=False, null=True)
    no_piezas = models.IntegerField(blank=False, null=False)
    a_cargo = models.ForeignKey(empleado, on_delete=models.DO_NOTHING, null=True)
    #fecha = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registro = models.CharField(max_length=99999999, blank=True, null=False)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.articulo_id)

class control_venta(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=99999999, choices=venta_status, blank=False, null=True)
    liquidacion_id = models.CharField(max_length=99999999, blank=True, null=True)
    cliente = models.ForeignKey(cliente, related_name='clientes_cosmeticos',on_delete=models.DO_NOTHING, default=u'system' )
    clienteid = models.IntegerField(blank=True, null=True)
    a_cuenta = models.IntegerField(blank=True, null=True)
    deve = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    pago_con = models.IntegerField(blank=True, null=True)
    fecha_pago = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    usuario = models.CharField(max_length=99999999, blank=False, null=False)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.pk)

    def get_absolute_url_venta(self):
        return reverse("cosmeticos:articulos_ventas", kwargs={"pk":self.pk})

    def get_url_add_article_venta_ticket(self):
        return reverse("Store:add_articles_view", kwargs={"pk":self.pk})

    def get_absolute_url_pago_contado(self):
        return reverse("Store:ticket_pago_contado", kwargs={"pk":self.pk})

    def get_absolute_url_apartado(self):
        return reverse("Store:ticket_pago_apartado", kwargs={"pk":self.pk})

class abonos_apartado(models.Model):
    id = models.AutoField(primary_key=True)
    control_venta_id = models.IntegerField(blank=True, null=True)
    id_cliente = models.IntegerField(blank=True, null=True)
    nombre_cliente = models.CharField(max_length=99999, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    saldo = models.IntegerField(blank=True, null=True)
    abono = models.IntegerField(blank=True, null=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.id)

class venta(models.Model):
    id = models.AutoField(primary_key=True)
    id_venta = models.IntegerField(blank=True, null=True)
    producto = models.CharField(max_length=99999999, blank=True, null=True)
    articulo_id = models.CharField(max_length=99999999, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    usuario = models.CharField(max_length=999999999, blank=True, null=False)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.id)


class liquidaciones_de_venta(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=999999, blank=True, null=True)
    liquido = models.IntegerField(blank=True, null=True)
    monto_a_liquidar = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" % (self.id)

    def __str__(self):
        return "%s" % (self.id)