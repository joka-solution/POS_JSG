from django.contrib import admin
from .models import inventario_global, inventario_store, cliente, control_venta, venta, control_almacen, empleado, abonos_apartado, liquidaciones_de_venta

# Register your models here.

class liquidaciones_de_ventaAdmin(admin.ModelAdmin):
    list_display = ["pk", "usuario", "liquido", "monto_a_liquidar", "balance", "registrado"]
    list_display_links = ["usuario"]
    class Meta:
        model = liquidaciones_de_venta

class empleadoModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "nombre", "direccion","telefono", "registrado"]
    list_display_links = ["nombre"]
    class Meta:
        model = empleado

class abonos_apartadoAdmin(admin.ModelAdmin):
    list_display = ["pk", "control_venta_id", "id_cliente", "nombre_cliente", "total", "abono", "saldo", "registrado"]
    list_display_links = ["nombre_cliente"]
    search_fields = ["control_venta_id", "id_cliente", "nombre_cliente"]
    class Meta:
        model = abonos_apartado

class inventario_globalModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "articulo_id", "nombre", "detalles", "imagen", "contenido_pzas", "precio_compra", "precio_distribucion", "precio_venta", "unidades_vendidas", "inventario", "inversion", "numero_caja", "barcode","registrado"]
    list_display_links = ["nombre"]
    # list_filter = ["overall_impact", "title"]
    search_fields = ["articulo_id", "nombre", "detalles"]
    class Meta:
        model = inventario_global

class inventario_storeModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "articulo_id", "nombre", "detalles", "imagen", "contenido_pzas", "precio_venta", "unidades_vendidas", "inventario", "barcode","registrado"]
    list_display_links = ["nombre"]
    # list_filter = ["overall_impact", "title"]
    search_fields = ["articulo_id", "nombre", "detalles"]
    class Meta:
        model = inventario_store

class control_almacenModelAdmin(admin.ModelAdmin):
    list_display = ["movimiento", "a_cargo", "articulo_id", "nombre", "no_piezas", "registro", "registrado"]
    list_display_links = ["articulo_id"]
    # list_filter = ["overall_impact", "title"]
    #search_fields = [" overall_impact", "title"]
    #search_fields = ["articulo_id", "nombre", "detalles", "a_cargo"]
    class Meta:
        model = control_almacen

class clienteModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "nombre", "apellido", "direccion", "email", "Telefono","descripcion", "registrado"]
    list_display_links = ["nombre"]
    class Meta:
        model = cliente

class control_ventaModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "status", "cliente", "cliente_id", "a_cuenta", "deve", "total", "pago_con", "fecha_pago", "usuario", "registrado"]
    list_display_links = ["cliente"]
    class Meta:
        model = control_venta

class ventaModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "id_venta","articulo_id", "producto", "cantidad", "precio", "total", "usuario", "registrado"]
    list_display_links = ["producto"]
    class Meta:
        model = venta

admin.site.register(inventario_global, inventario_globalModelAdmin)
admin.site.register(inventario_store, inventario_storeModelAdmin)
admin.site.register(control_almacen,control_almacenModelAdmin)
admin.site.register(cliente, clienteModelAdmin)
admin.site.register(control_venta, control_ventaModelAdmin)
admin.site.register(venta, ventaModelAdmin)
admin.site.register(empleado, empleadoModelAdmin)
admin.site.register(abonos_apartado, abonos_apartadoAdmin)
admin.site.register(liquidaciones_de_venta, liquidaciones_de_ventaAdmin)
