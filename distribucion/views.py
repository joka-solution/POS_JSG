from django.contrib import messages
from bootstrap_datepicker_plus import DateTimePickerInput
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.db.models import Sum
from datetime import datetime, date, time, timedelta
from pytz import timezone
from .models import inventario_distribucion, control_venta_distribucion, control_agregar_inventario_dist, control_devolucion_inventario_dist
from Store.models import empleado
from .forms import Add_Article_inventory_Distr_Form
import re
import barcode
from barcode.writer import ImageWriter
import logging


# Create your views here.


def articulos_inventario_distribucion(request):
    query_list = inventario_distribucion.objects.all().order_by('-pk')

    # =======================================
    suma = inventario_distribucion.objects.all().aggregate(Sum('precio_venta'))

    user = request.user
    logging.critical("Usuario: %s" % user)

    totales_list = []

    '''for x in inventario_distribucion.objects.all():
        precio = x.precio_venta
        precio = int(precio)
        piezas = x.inventario
        piezas = int(piezas)
        total = precio * piezas

        totales_list.append(total)

        articulo_id = x.articulo_id

        index = x.pk
        nombre = x.nombre
        detalles = x.detalles
        contenido_pzas = x.contenido_pzas
        precio_venta = x.precio_venta
        inventario = x.inventario
        existencia = x.inventario
        inversion = x.inversion
        monto_total = total

        unidades_vendidas = x.unidades_vendidas

        # ++++++++++++++++++++++++++++++++
        if x.barcode:
            logging.critical("el Barcode Existe!!")
            logging.critical("Filename: %s" % x.barcode)
            filename = x.barcode
        else:
            logging.critical("el Barcode NO Existe!!")
            registro = get_object_or_404(inventario_distribucion, pk=x.pk)
            lineCode = registro.articulo_id
            logging.critical("Barcode: %s" % lineCode)
            barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
            barcodeName = lineCode + "_barcode"
            barcodeNameReg = '/Users/jaime/Projects/POS_JSG/media/BarCode/' + barcodeName
            barcodeNameRegAd = 'BarCode/' + barcodeName + ".png"
            filename = barCodeImage.save(barcodeNameReg)
            logging.critical("Print Barcode: %s" % filename)
            registro.barcode = barcodeNameRegAd
            registro.save()
        # ++++++++++++++++++++++++++++++++

    gran_total = 0
    for i in totales_list:
        gran_total = gran_total + i

    logging.critical("La Suma Global es de: %s", gran_total)'''

    # =======================================
    paginator = Paginator(query_list, 200)
    page_request_var = "historic"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if request.method == 'POST' and 'nuevo_articulo_distr' in request.POST:
        return redirect('../add_new_article_inventario_distr')

    if request.method == 'POST' and 'liquidacion' in request.POST:
        user = request.user
        nombre_cliente='Carmen'
        id_cliente = empleado.objects.filter(nombre='%s' % nombre_cliente)
        logging.critical("id del distribuidor: %s" % id_cliente.pk)

        venta = control_venta_distribucion(cliente=nombre_cliente, clienteid=id_cliente.pk, usuario=user)
        venta.save()

        logging.critical("Index de la venta: %s" % venta.pk)
        return HttpResponseRedirect(venta.get_url_add_article_venta_dist_ticket())

        #return redirect('../liquidacion_distribucion')

    '''if request.method == 'POST' and 'Agregar' in request.POST:
        v1 = request.POST['buscala']
        v2 = 'prueba'
        id_producto=inventario_distribucion.objects.filter(nombre=v2)
        instance = inventario_distribucion.objects.get(nombre='%s' % v1)

        logging.critical("Este es el valor de Buscando: %s" % v1)
        logging.critical("Este es el valor del index Buscando: %s" % instance.pk)'''

    if request.method == 'POST' and 'Agregar' in request.POST:
        user = request.user
        nombre_cliente = 'Carmen'
        #id_cliente = empleado.objects.filter(nombre='%s' % nombre_cliente)
        #logging.critical("id del distribuidor: %s" % id_cliente.nombre)
        #logging.critical("id del distribuidor: %s" % id_cliente.pk)
        v1 = request.POST['valor']
        index = request.POST.get('indice')
        cantidad = int(v1)
        instance = inventario_distribucion.objects.get(pk=index)
        resultado = instance.inventario + cantidad
        monto_total = instance.precio_dist * resultado
        registro = control_agregar_inventario_dist(usuario=user, articulo_id=instance.articulo_id, nombre=instance, inventario_antes=instance.inventario, se_agregaron=cantidad, inventario_despues=resultado)
        registro.save()
        instance.inventario = resultado
        instance.monto = monto_total
        instance.save()

    if request.method == 'POST' and 'Devolver' in request.POST:
        user = request.user
        nombre_cliente = 'Carmen'
        #id_cliente = empleado.objects.filter(nombre='%s' % nombre_cliente)
        #logging.critical("id del distribuidor: %s" % id_cliente.nombre)
        #logging.critical("id del distribuidor: %s" % id_cliente.pk)
        v1 = request.POST['valor']
        index = request.POST.get('indice')
        cantidad = int(v1)
        instance = inventario_distribucion.objects.get(pk=index)
        resultado = instance.inventario - cantidad
        monto_total = instance.precio_dist * resultado
        registro = control_devolucion_inventario_dist(usuario=user, articulo_id=instance.articulo_id, nombre=instance, inventario_antes=instance.inventario, se_agregaron=cantidad, inventario_despues=resultado)
        registro.save()
        instance.inventario = resultado
        instance.monto=monto_total
        instance.save()

    if request.method == 'POST' and 'crear_liquidacion' in request.POST:
        user = request.user
        #nombre_cliente = 'Carmen'
        #id_cliente = empleado.objects.filter(nombre='%s' % nombre_cliente)
        # logging.critical("id del distribuidor: %s" % id_cliente.nombre)
        # logging.critical("id del distribuidor: %s" % id_cliente.pk)
        venta = control_venta_distribucion(status='Abierta', usuario=user)
        venta.save()
        logging.critical("Index de la venta: %s" % venta.pk)

        #return HttpResponseRedirect(venta.get_url_add_article_venta_ticket())

    if request.method == 'POST' and 'Liquidar' in request.POST:
        user = request.user
        v1 = request.POST['valor']
        index = request.POST.get('indice')
        cantidad = int(v1)
        instance = inventario_distribucion.objects.get(pk=index)
        resultado = instance.inventario - cantidad
        monto_total = instance.precio_dist * resultado
        registro = control_devolucion_inventario_dist(usuario=user, articulo_id=instance.articulo_id, nombre=instance,
                                                      inventario_antes=instance.inventario, se_agregaron=cantidad,
                                                      inventario_despues=resultado)
        #registro.save()
        instance.inventario = resultado
        instance.monto = monto_total
        #instance.save()

    if control_venta_distribucion.objects.get(status='Abierta'):
        valor1 = control_venta_distribucion.objects.get(status='Abierta')
        logging.critical("El valor es: %s" % valor1)
        status = 'Abierta'
        num_liq = control_venta_distribucion.objects.filter(status='Abierta')
    else:
        status = 'nada'
        num_liq = 'nada'


    context = {
        "title": 'Inventario Distribucion Bella Donna.',
        "object_list": queryset,
        "page_request_var": page_request_var,
        "liq_status": status,
        "num_liq": num_liq,
        # "imgbarcode": filename,
        # "name": 'ean13.png',
    }
    return render(request, "inventario_distribucion.html", context)



def add_articles_dist_view(request, pk=None):
    cv = get_object_or_404(control_venta_distribucion, pk=pk)
    user = request.user

    if cv.clienteid == 1:
        flag_01 = 'SYSTEM'
        logging.critical("El USUARIO ES SYSTEM!!!")
    else:
        flag_01 = 'apartados'
        logging.critical("NO ES EL USUARIO SYSTEM!!!")

    add_article = add_articles_Form(request.POST or None, request.FILES or None)
    #pago_form = pago_con_Form(request.POST or None, request.FILES or None)
    #encabezado = 'Agregar Articulos al Folio: %s, Cliente: %s' % (cv.pk, cv.cliente)

    if request.method == 'POST' and 'add_article' in request.POST:
        if add_article.is_valid():
            # Obtiene loda valores ingresados en el Formulario
            nombre_art = add_article.cleaned_data['articulo_id']
            cantidad_art = add_article.cleaned_data['cantidad']
            cuenta_nombre_art = len(nombre_art)

            logging.critical("#====================== 1 ============================")
            logging.critical("Folio de Control de Venta: %s" % cv.pk)
            logging.critical("Nombre del Cliente: %s" % cv.cliente)
            logging.critical("#====================== 2 ============================")
            logging.critical("Articulo: %s" % nombre_art)

            if inventario_store.objects.get(articulo_id=nombre_art):
                articulo = inventario_store.objects.get(articulo_id=nombre_art)
                logging.critical("Precio: %s" % articulo.precio_venta)
                logging.critical("Nombre: %s" % articulo.nombre)
            else:
                messages.success(request, "<center><a href='#'>EL ARTICULO NO EXISTE!!!</a></center> Updated", extra_tags='html_safe')
                logging.critical("El Articulo: %s, NO EXISTE!!!" % nombre_art)

            logging.critical("#====================== 3 ============================")

            cantidad = venta.objects.filter(id_venta=cv, articulo_id=nombre_art)
            cantidad_articulos = len(cantidad)
            logging.critical("Cantidad del mismo articulo: %s" % cantidad_articulos)

            if articulo.inventario > cantidad_art:
                logging.critical("SI HAY SUFICIENTES ARTICULOS PARA SURTIR ESTE PEDIDO!!!")
            else:
                messages.success(request, "<center><a href='#'>NO HAY SUFICIENTES ARTICULOS PARA SURTIR ESTE PEDIDO!!!</a></center> Updated", extra_tags='html_safe')
                logging.critical("NO HAY SUFICIENTES ARTICULOS PARA SURTIR ESTE PEDIDO!!!")
            # Contar cuantos articulos estan en el mismo ticket.
            v1 = venta.objects.filter(id_venta=cv)
            cuenta = len(v1)
            logging.critical("Cuenta Total de Articulos en el mismo Ticket: %s" % cuenta)

            if cuenta == 0:
                logging.critical("========= Fase 1 conteo = 0 no hay ningun articulo en este folio ================")
                instancia = add_article.save(commit=False)
                # instancia.save()
                # REALIZAR OPERACIONES
                total_x_articulo = articulo.precio_venta * cantidad_art
                registro = venta(id_venta=cv, producto=articulo.nombre, articulo_id=nombre_art,
                                 cantidad=cantidad_art, precio=articulo.precio_venta, total=total_x_articulo,
                                 usuario=user)
                registro.save()
            else:
                if cantidad.exists():
                    for x in cantidad:
                        logging.critical(
                            "========= Fase 3 Ya existe algun articulo similar en el folio ================")
                        logging.critical("El Articulo ya esta en la lista!!")
                        logging.critical("La Cantidad de V1 es: %s" % x.cantidad)
                        logging.critical("La Cantidad a agregar en V1 es de: %s" % cantidad_art)
                        logging.critical("El Precio es de: %s" % x.precio)
                        logging.critical("El Index del registro es: %s" % x.pk)

                        total_int = x.cantidad + cantidad_art
                        total_x_articulo = total_int * x.precio

                        REGISTRO = get_object_or_404(venta, pk=x.pk)
                        REGISTRO.cantidad = total_int
                        REGISTRO.total = total_x_articulo
                        REGISTRO.save()
                        logging.critical(
                            "========= Termina Fase 3 Folio: %s ================" % x.pk)
                else:
                    logging.critical(
                        "========= Fase 4 Ya existen articulos en el ticket pero ninguno similar en este folio ================")
                    logging.critical("El Articulo NO esta en la lista!!")
                    # REALIZAR OPERACIONES
                    total_x_articulo = articulo.precio_venta * cantidad_art
                    registro = venta(id_venta=cv, producto=articulo.nombre, articulo_id=nombre_art,
                                     cantidad=cantidad_art, precio=articulo.precio_venta, total=total_x_articulo,
                                     usuario=user)
                    registro.save()
                    logging.critical(
                        "========= Termina Fase 4 Folio: %s ================")

            add_article = add_articles_Form(request.POST or None, request.FILES or None)

        lista_venta = venta.objects.filter(id_venta=cv)
        cuenta_lista_venta = len(lista_venta)
        logging.critical("El Conteo de Lista Venta es de: %s" % cuenta_lista_venta)

        if cuenta_lista_venta > 0:
            imagen = articulo.imagen
            totales_lista = []
            for x in venta.objects.filter(id_venta=cv):
                totales_lista.append(x.total)

            gran_total = 0
            for i in totales_lista:
                gran_total = gran_total + i

            # Registrando el Total de la cuenta en la DB en la tabla de Control de Ventas.
            # total_registro = control_venta.objects.get(pk=pk)
            cv.total = gran_total
            cv.save()
            logging.critical("El Gran TOTAL es : %s", gran_total)

            context = {
                "title": encabezado,
                "form": add_article,
                "queryset": lista_venta,
                'total': gran_total,
                'imagen': imagen,
                "flag": flag_01,
                # 'pago_form': pago_form,
            }
            return render(request, "ventas_add_articles.html", context)

    if request.method == 'POST' and 'contado' in request.POST:
        logging.critical("Entre en modo Contado")
        return HttpResponseRedirect(cv.get_absolute_url_pago_contado())

    if request.method == 'POST' and 'apartados' in request.POST:
        logging.critical("Entre en modo Apartado")
        return HttpResponseRedirect(cv.get_absolute_url_apartado())

    context = {
        "title": encabezado,
        "form": add_article,
        "flag": flag_01,
        # "queryset": lista_venta,
        # 'total': gran_total,
        # 'imagen': img,
    }
    return render(request, "ventas_add_articles.html", context)

def add_new_article_inventario_distr(request):
    form = Add_Article_inventory_Distr_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'agregar_articulo' in request.POST:
        if form.is_valid():
            # registro = form.cleaned_data['articulo_id']
            form.save()
            # ++++++++++++++++++++++++++++++++


            # ++++++++++++++++++++++++++++++++
            return redirect('../inventario&Dist')
    context = {
        "title": 'Agregar nuevo Articulo al Inventario.',
        "form": form,
    }
    return render(request, "add_article_distribution_inventory.html", context)
