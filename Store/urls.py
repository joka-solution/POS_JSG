from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    articulos_inventario_global,
    articulos_inventario_store,
    articulos_inventario_test,
    edit_images,
    control_almacen_view,
    control_cargo_view,
    ventas_view,
    add_articles_view,
    add_new_article_to_inventario_global,
    add_new_article_to_inventario_store,
    add_new_cliente,
    corte_ventas,
    pago_contado,
    pago_apartado,
    create_ticket,
    clientes_view,
    cliente_detalle_view,
)

# , clientes_list, articulos_inventario,articulos_ventas, venta_de_productos, articulos_venta_ticket, BookListView

#

urlpatterns = [
    # url(r'^articulos/', articulos_list, name='cosmeticos_articulos'),
    # url(r'^(?P<pk>\d+)/articulos_venta/$', articulos_ventas, name='articulos_ventas'),
    # url(r'^(?P<pk>\d+)/articulos_venta/ticket/$', articulos_venta_ticket, name='articulos_venta_ticket'),

    # url(r'^clientes/', clientes_list, name='cosmeticos_clientes'),
    url(r'^inventario&Global/', articulos_inventario_global, name='inventario_global'),
    url(r'^inventario&Store&0_1/', articulos_inventario_store, name='inventario_store'),
    url(r'^add_new_article_inventario_global/', add_new_article_to_inventario_global, name='add_new_articles_global'),
    url(r'^add_new_article_inventario_store/', add_new_article_to_inventario_store, name='add_new_articles_store'),
    url(r'^add_new_cliente/', add_new_cliente, name='add_new_cliente'),
    url(r'^corte_ventas/', corte_ventas, name='corte_de_ventas'),
    url(r'^clientes_list/', clientes_view, name='clientes_list'),
    # url(r'^control_almacen/$', control_almacen, name='Control_Almacen'),

    url(r'^(?P<pk>\d+)/editimage/$', edit_images, name='editimage'),
    url(r'^(?P<pk>\d+)/control_almacen/$', control_almacen_view, name='add_or_remove_inventory'),
    url(r'^Control_Almacen_Cargo/$', control_cargo_view, name='Control_Cargo'),
    url(r'^Generar_Venta/$', ventas_view, name='ventas'),
    url(r'^(?P<pk>\d+)/add_articles/$', add_articles_view, name='add_articles_view'),
    url(r'^(?P<pk>\d+)/ticket_contado/$', pago_contado, name='ticket_pago_contado'),
    url(r'^(?P<pk>\d+)/ticket_apartado/$', pago_apartado, name='ticket_pago_apartado'),
    url(r'^(?P<pk>\d+)/ticket_to_print/$', create_ticket, name='createticket'),
    url(r'^(?P<pk>\d+)/cliente_detalle/$', cliente_detalle_view, name='clientedetalleview'),
    # pruebas
    # url(r'^venta_productos/', venta_de_productos, name='venta_prod'),
    # url(r'^list/', BookListView.as_view(), name='book_list'),
]