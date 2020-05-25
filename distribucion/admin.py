from django.contrib import admin
from .models import inventario_distribucion, control_agregar_inventario_dist, control_devolucion_inventario_dist, control_venta_distribucion

# Register your models here.


class inventario_distribucionAdmin(admin.ModelAdmin):
    list_display = ["pk", "a_cargo","articulo_id", "nombre", "detalles", "contenido_pzas", "precio_dist", "precio_venta", "inventario", "registrado"]
    list_display_links = ["nombre"]
    class Meta:
        model = inventario_distribucion

class control_agregar_articulos_distribucionAdmin(admin.ModelAdmin):
    list_display = ["pk", "usuario","distribuidor", "articulo_id", "nombre", "inventario_antes", "se_agregaron", "inventario_despues", "registrado"]
    list_display_links = ["nombre"]
    class Meta:
        model = control_agregar_inventario_dist

class control_devolucion_inventario_distribucionAdmin(admin.ModelAdmin):
    list_display = ["pk", "usuario","distribuidor", "articulo_id", "nombre", "inventario_antes", "se_agregaron", "inventario_despues", "registrado"]
    list_display_links = ["nombre"]
    class Meta:
        model = control_devolucion_inventario_dist

class control_venta_distribucionModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "status", "distribuidor", "clienteid", "a_cuenta", "deve", "total", "pago_con", "fecha_pago", "usuario", "registrado"]
    list_display_links = ["distribuidor"]
    class Meta:
        model = control_venta_distribucion

admin.site.register(inventario_distribucion, inventario_distribucionAdmin)
admin.site.register(control_agregar_inventario_dist, control_agregar_articulos_distribucionAdmin)
admin.site.register(control_devolucion_inventario_dist, control_devolucion_inventario_distribucionAdmin)
admin.site.register(control_venta_distribucion, control_venta_distribucionModelAdmin)