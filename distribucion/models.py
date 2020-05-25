from __future__ import unicode_literals
from django.conf import settings
from django.urls import reverse
from django.db import models
from Store.models import empleado

#Models

venta_status = (
    ('Abierta', 'Abierta'),
    ('Pendiente', 'Pendiente'),
    ('Apartado', 'Apartado'),
    ('Cancelada', 'Cancelada'),
    ('Cerrada', 'Cerrada'),
    ('Concesion', 'Concesion'),
    ('Liquidado', 'Liquidado'),
)


class inventario_distribucion(models.Model):
    id = models.AutoField(primary_key=True)
    a_cargo = models.ForeignKey(empleado, on_delete=models.DO_NOTHING, null=True)
    articulo_id = models.CharField(max_length=99999999, blank=True, null=True, unique=True)
    imagen = models.ImageField(upload_to = 'Articulos/', blank=True, null=True)
    barcode = models.ImageField(upload_to = 'BarCode/', blank=True, null=True)
    nombre = models.CharField(max_length=99999999, blank=False, null=False, unique=True)
    detalles = models.CharField(max_length=99999999, blank=True, null=True)
    contenido_pzas = models.CharField(max_length=99999999, blank=True, null=False)
    #PRECIOS
    precio_dist = models.IntegerField(null=True, blank=True)
    precio_venta = models.IntegerField(null=True, blank=True)
    #INVENTARIOS ALMACEN GLOBAL
    inventario = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField(null=True, blank=True)
    #unidades_vendidas = models.CharField(max_length=99999999, null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.nombre)

class control_agregar_inventario_dist(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=99999999, blank=False, null=False)
    distribuidor = models.ForeignKey(empleado, on_delete=models.DO_NOTHING, null=True, blank=True)
    articulo_id = models.CharField(max_length=99999999, blank=True, null=True, unique=True)
    nombre = models.CharField(max_length=99999999, blank=False, null=False)
    inventario_antes = models.IntegerField(null=True, blank=True)
    se_agregaron = models.IntegerField(null=True, blank=True)
    inventario_despues = models.IntegerField(null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.nombre)

class control_devolucion_inventario_dist(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=99999999, blank=False, null=False)
    distribuidor = models.ForeignKey(empleado, on_delete=models.DO_NOTHING, null=True, blank=True)
    articulo_id = models.CharField(max_length=99999999, blank=True, null=True, unique=True)
    nombre = models.CharField(max_length=99999999, blank=False, null=False)
    inventario_antes = models.IntegerField(null=True, blank=True)
    se_agregaron = models.IntegerField(null=True, blank=True)
    inventario_despues = models.IntegerField(null=True, blank=True)
    registrado = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return u"%s" %(self.id)

    def __str__(self):
        return "%s" %(self.nombre)

class control_venta_distribucion(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=99999999, choices=venta_status, blank=False, null=True)
    distribuidor = models.ForeignKey(empleado, on_delete=models.DO_NOTHING, null=True, blank=True)
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
        return "%s" %(self.distribuidor)

    #def get_absolute_url_venta(self):
    #    return reverse("cosmeticos:articulos_ventas", kwargs={"pk":self.pk})

    def get_url_add_article_venta_dist_ticket(self):
        return reverse("distribucion:add_articles_dist_view", kwargs={"pk":self.pk})

    def get_absolute_url_pago_contado(self):
        return reverse("Store:ticket_pago_contado", kwargs={"pk":self.pk})

    def get_absolute_url_apartado(self):
        return reverse("Store:ticket_pago_apartado", kwargs={"pk":self.pk})


class venta_distribucion(models.Model):
    id_venta = models.ForeignKey(
        control_venta_distribucion,
        models.SET_NULL,
        blank=True,
        null=True,
        )
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
