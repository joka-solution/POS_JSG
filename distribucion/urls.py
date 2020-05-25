from django.conf.urls import url, include
from django.contrib import admin
from .views import (
    articulos_inventario_distribucion,
    add_new_article_inventario_distr,
    add_articles_dist_view,
)

# , clientes_list, articulos_inventario,articulos_ventas, venta_de_productos, articulos_venta_ticket, BookListView

#

urlpatterns = [
    url(r'^inventario&Dist/', articulos_inventario_distribucion, name='inventario_distribucion'),
    url(r'^add_new_article_inventario_distr/', add_new_article_inventario_distr, name='add_new_article_inventario_distr'),
    url(r'^(?P<pk>\d+)/add_articles_dist/$', add_articles_dist_view, name='add_articles_dist_view'),
]