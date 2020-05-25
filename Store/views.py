from django.contrib import messages
from bootstrap_datepicker_plus import DateTimePickerInput
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Sum
from datetime import datetime, date, time, timedelta
from time import gmtime, strftime
from pytz import timezone
from .models import inventario_global, inventario_store, control_almacen, control_venta, venta, cliente, \
    abonos_apartado, liquidaciones_de_venta # ,cliente,control_venta, venta, Book
from .forms import Contro_AlmacenForm, imageForm, cargo_persona_Form, New_Venta_Form, add_articles_Form, pago_con_Form, \
    Add_Article_inventory_Form, register_new_clientForm, corte_select_userForm, \
    a_cuenta_Form, Add_Article_inventory_Store_Form  # , AuthorFormset, form_fecha_pago, fecha_form, form_select_cliente, form_cantidad_articulos
# from .models import Book, Author
# import treepoem
import re
import barcode
from barcode.writer import ImageWriter
import logging

barcode_path = '/Users/jaimesanchez/Documents/School/Project/POS_JSG/media/BarCode'

# Create your views here.

def edit_images(request, pk=None):
    instance = get_object_or_404(inventario_global, pk=pk)
    form = imageForm(request.POST or None, request.FILES or None, instance=instance)

    logging.critical("Instance: %s" % instance)

    if request.method == 'POST' and 'change_img' in request.POST:
        if form.is_valid():
            logging.critical("paso la validacion")
            instance = form.save(commit=False)
            instance.save()
            return redirect('../../inventario&Global')
        else:
            logging.critical("no paso la validacion")

    context = {
        "title": "Cambiar Imagen.",
        "form": form,
    }
    return render(request, "edit_images.html", context)


def control_almacen_view(request, pk=None):
    instance = get_object_or_404(inventario_global, pk=pk)
    control_almacen_form = Contro_AlmacenForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and 'control_almacen' in request.POST:
        if control_almacen_form.is_valid():
            user = request.user
            instance.nombre = instance.nombre
            instance.articulo_id = instance.articulo_id
            instance.precio_distribucion = instance.precio_distribucion
            # ================================================================
            numero_piezas = control_almacen_form.cleaned_data['no_piezas']
            accion = control_almacen_form.cleaned_data['movimiento']
            acargo = control_almacen_form.cleaned_data['a_cargo']

            if 'Entrada' in accion:
                no_total = instance.existencia + numero_piezas

                if no_total > instance.existencia:
                    messages.warning(request,
                                     "No se actualizo el Articulo: %s, devido a no coincide con el numero de existencia." % instance.nombre)
                    return redirect('../../inventario')
                elif no_total <= instance.existencia:
                    instance.existencia = no_total
                    monto_total = instance.precio_venta * no_total
                    instance.monto_total = monto_total
                    instance.save()
                    registro = control_almacen(articulo_id=instance.articulo_id, nombre=instance.nombre,
                                               movimiento=accion, no_piezas=numero_piezas, a_cargo=acargo,
                                               registro=user)
                    registro.save()
                    messages.success(request, "Se Actualizado Correctamente el Articulo: %s" % instance.nombre)
                    return redirect('../../inventario')

            elif 'Salida' in accion:
                no_total = instance.existencia - numero_piezas

                if no_total < 0:
                    messages.warning(request,
                                     "No se actualizo el Articulo: %s, devido a no coincide con el numero de existencia." % instance.nombre)
                    return redirect('../../inventario')
                elif no_total >= 0 and no_total <= instance.existencia:
                    messages.success(request, "Se Actualizado Correctamente el Articulo: %s" % instance.nombre)
                    instance.existencia = no_total
                    monto_total = instance.precio_venta * no_total
                    instance.monto_total = monto_total
                    instance.save()
                    registro = control_almacen(articulo_id=instance.articulo_id, nombre=instance.nombre,
                                               movimiento=accion, no_piezas=numero_piezas, a_cargo=acargo,
                                               registro=user)
                    registro.save()
                    return redirect('../../inventario')
            else:
                return redirect('../../inventario')

    context = {
        "title": 'Control Entradas y Salidas de Almacen.',
        "form": control_almacen_form,
        # "page_request_var": page_request_var,
    }
    return render(request, "Control_Almacen.html", context)


def control_cargo_view(request):
    cargo_persona = cargo_persona_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'persona_seleccionada' in request.POST:
        if cargo_persona.is_valid():
            persona = cargo_persona.cleaned_data['a_cargo']
            logging.critical("Persona: %s" % persona)
            queryset = control_almacen.objects.filter(a_cargo=persona)
            global_query = inventario_global.objects.all()

            for x in queryset:
                logging.critical(x)

            context = {
                "title": 'Nueva prueba.',
                "query": queryset,
                "global_query": global_query,

            }
            return render(request, "Bella_Donna_Control_Vista_Cargo_Persona.html", context)

    context = {
        "title": 'Vista de articulos a Cargo.',
        "form": cargo_persona,
    }
    return render(request, "Bella_Donna_Control_Almacen_vista.html", context)


def articulos_inventario_test(request):
    queryset_list = inventario_global.objects.all().order_by('-pk')
    paginator = Paginator(queryset_list, 500)
    page_request_var = "sopaprove"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "Pending Approval.",
        # "count": count_new,
        # "objects_status": queyrset_status,
        "object_list": queryset,
        # "page_request_var": page_request_var,
        # "modelo": modelo2,
        # "horarios": horarios,
    }
    return render(request, "Bella_Donna_inventario.html", context)  # OK


def articulos_inventario_global(request):
    query_list = inventario_global.objects.all().order_by('-pk')
    # =======================================
    suma = inventario_global.objects.all().aggregate(Sum('precio_venta'))
    logging.critical("@@---@@ La Suma es: %s" % suma)
    user = request.user
    logging.critical("Usuario: %s" % user)

    totales_list = []

    for x in inventario_global.objects.all():
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

        # cantidad_entrada = x.cantidad_entrada

        precio_compra = x.precio_compra
        precio_distribucion = x.precio_distribucion
        precio_venta = x.precio_venta

        inventario = x.inventario
        existencia = x.inventario
        inversion = x.inversion
        monto_total = total

        unidades_vendidas = x.unidades_vendidas
        numero_caja = x.numero_caja

        # ++++++++++++++++++++++++++++++++
        if x.barcode:
            logging.critical("el Barcode Existe!!")
            logging.critical("Filename: %s" % x.barcode)
            filename = x.barcode
        else:
            logging.critical("el Barcode NO Existe!!")
            registro = get_object_or_404(inventario_global, pk=x.pk)
            lineCode = registro.articulo_id
            logging.critical("Barcode: %s" % lineCode)

            EAN = barcode.get_barcode_class('ean13')
            ean = EAN(lineCode, writer=ImageWriter())
            barcodeName = lineCode + "_barcode"
            barcodeNameReg = '/Users/jaimesanchez/Documents/School/Project/POS_JSG/media/BarCode/' + barcodeName
            barcodeNameRegAd = 'BarCode/' + barcodeName + ".png"
            fullname = ean.save(barcodeNameReg)

            '''barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
            barcodeName = lineCode + "_barcode"
            barcodeNameReg = '/Users/jaimesanchez/Documents/School/Project/POS_JSG/media/BarCode/' + barcodeName
            barcodeNameRegAd = 'BarCode/' + barcodeName + ".png"
            filename = barCodeImage.save(barcodeNameReg)'''
            logging.critical("Print Barcode: %s" % filename)
            registro.barcode = barcodeNameRegAd
            registro.save()
        # ++++++++++++++++++++++++++++++++

    gran_total = 0
    for i in totales_list:
        gran_total = gran_total + i

    logging.critical("La Suma Global es de: %s", gran_total)

    # =======================================
    paginator = Paginator(query_list, 500)
    page_request_var = "historic"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    if request.method == 'POST' and 'nuevo_articulo_global' in request.POST:
        return redirect('../add_new_article_inventario_global')
    # ++++++++++++++++++++++++++++++++
    # ean = barcode.get('ean13', '123456789102', writer=ImageWriter())
    # filename = ean.save('/Users/jaime/Projects/MOBA/media/Articulos/ean13')
    # ++++++++++++++++++++++++++++++++
    # image = treepoem.generate_barcode(
    #   barcode_type='qrcode',

    #    data='barcode payload',
    # )
    # image.convert('1').save('/Users/jaime/Projects/MOBA/media/Articulos/prueba1_barcode.png')
    '''# ++++++++++++++++++++++++++++++++
    registro = get_object_or_404(inventario_global, pk=6)
    lineCode =registro.articulo_id
    barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
    barcodeName = lineCode + "barcode"
    barcodeNameReg = '/Users/jaime/Projects/POS_JSG/media/BarCode/' + barcodeName
    barcodeNameRegAd = 'BarCode/' + barcodeName + ".png"
    filename = barCodeImage.save(barcodeNameReg)
    logging.critical("Print Barcode: %s" % filename)
    registro.barcode = barcodeNameRegAd
    registro.save()
    # ++++++++++++++++++++++++++++++++'''
    context = {
        "title": 'Inventario Global.',
        "object_list": queryset,
        "page_request_var": page_request_var,
        #"imgbarcode": filename,
        # "name": 'ean13.png',
    }
    return render(request, "inventario_global.html", context)

def articulos_inventario_store(request):
    query_list = inventario_store.objects.all().order_by('-pk')
    # =======================================
    suma = inventario_store.objects.all().aggregate(Sum('precio_venta'))
    logging.critical("@@---@@ La Suma es: %s" % suma)
    user = request.user
    logging.critical("Usuario: %s" % user)

    totales_list = []

    for x in inventario_store.objects.all():
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
        #inversion = x.inversion
        monto_total = total

        unidades_vendidas = x.unidades_vendidas

        # ++++++++++++++++++++++++++++++++
        if x.barcode:
            logging.critical("el Barcode Existe!!")
            logging.critical("Filename: %s" % x.barcode)
            filename = x.barcode
        else:
            logging.critical("el Barcode NO Existe!!")
            registro = get_object_or_404(inventario_store, pk=x.pk)
            lineCode = registro.articulo_id
            logging.critical("Barcode: %s" % lineCode)
            barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
            barcodeName = lineCode + "_barcode"
            barcodeNameReg = '/Users/jaimesanchez/Documents/School/Project/POS_JSG/media/BarCode/' + barcodeName
            logging.critical("path: %s" % barcodeNameReg)
            barcodeNameRegAd = 'BarCode/' + barcodeName + ".png"
            filename = barCodeImage.save(barcodeNameReg)
            logging.critical("Print Barcode: %s" % filename)
            registro.barcode = barcodeNameRegAd
            registro.save()
        # ++++++++++++++++++++++++++++++++

    gran_total = 0
    for i in totales_list:
        gran_total = gran_total + i

    logging.critical("La Suma Global es de: %s", gran_total)

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

    if request.method == 'POST' and 'nuevo_articulo_store' in request.POST:
        return redirect('../add_new_article_inventario_store')
    # ++++++++++++++++++++++++++++++++
    # ean = barcode.get('ean13', '123456789102', writer=ImageWriter())
    # filename = ean.save('/Users/jaime/Projects/MOBA/media/Articulos/ean13')
    # ++++++++++++++++++++++++++++++++
    # image = treepoem.generate_barcode(
    #   barcode_type='qrcode',

    #    data='barcode payload',
    # )
    # image.convert('1').save('/Users/jaime/Projects/MOBA/media/Articulos/prueba1_barcode.png')
    '''# ++++++++++++++++++++++++++++++++
    registro = get_object_or_404(inventario_global, pk=6)
    lineCode =registro.articulo_id
    barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
    barcodeName = lineCode + "barcode"
    barcodeNameReg = '/Users/jaime/Projects/POS_JSG/media/BarCode/' + barcodeName
    barcodeNameRegAd = 'BarCode/' + barcodeName + ".png"
    filename = barCodeImage.save(barcodeNameReg)
    logging.critical("Print Barcode: %s" % filename)
    registro.barcode = barcodeNameRegAd
    registro.save()
    # ++++++++++++++++++++++++++++++++'''
    context = {
        "title": 'Inventario Bella Donna Tienda.',
        "object_list": queryset,
        "page_request_var": page_request_var,
        #"imgbarcode": filename,
        # "name": 'ean13.png',
    }
    return render(request, "inventario_store.html", context)


def add_new_article_to_inventario_global(request):
    form = Add_Article_inventory_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'agregar_articulo' in request.POST:
        if form.is_valid():
            # registro = form.cleaned_data['articulo_id']
            form.save()
            # ++++++++++++++++++++++++++++++++
            '''lineCode =registro
            barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
            filename = barCodeImage.save('/Users/jaime/Projects/MOBA/POS_JSG/BarCode/prueba2_barcode')
            logging.critical("Print Barcode: %s" % filename)'''

            # ++++++++++++++++++++++++++++++++
            return redirect('../inventario&Global')
    context = {
        "title": 'Agregar nuevo Articulo al Inventario Global.',
        "form": form,
    }
    return render(request, "add_article_global_inventory.html", context)

def add_new_article_to_inventario_store(request):
    form = Add_Article_inventory_Store_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'agregar_articulo' in request.POST:
        if form.is_valid():
            registro = form.cleaned_data['articulo_id']
            logging.critical("Valor Articulo ID: %s" % registro)
            #form.save()
            # ++++++++++++++++++++++++++++++++
            '''lineCode =registro
            barCodeImage = barcode.get('ean13', lineCode, writer=ImageWriter())
            filename = barCodeImage.save('/Users/jaime/Projects/POS_JSG/media/BarCode/prueba2_barcode')
            logging.critical("Print Barcode: %s" % filename)'''

            # ++++++++++++++++++++++++++++++++
            return redirect('../inventario&Store&0_1')
    context = {
        "title": 'Agregar nuevo Articulo al Inventario.',
        "form": form,
    }
    return render(request, "add_article_global_inventory.html", context)


def add_new_cliente(request):
    form = register_new_clientForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'agregar_articulo' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('../Generar_Venta')
    context = {
        "title": 'Registrar Nuevo Cliente.',
        "form": form,
    }
    return render(request, "Registrar_nuevo_cliente.html", context)


def ventas_view(request):
    user = request.user
    nombre_tienda = New_Venta_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'cliente_seleccionado' in request.POST:
        if nombre_tienda.is_valid():
            nombre = nombre_tienda.cleaned_data['cliente']
            id_cliente = cliente.objects.get(nombre=nombre)

            logging.critical("PK del Cliente desde clientes: %s" % id_cliente.pk)
            logging.critical("Nombre del Cliente: %s" % nombre)
            venta = control_venta(status='Abierta', cliente=nombre, clienteid=id_cliente.pk, usuario=user)
            venta.save()

            logging.critical("Index de la venta: %s" % venta.pk)
            return HttpResponseRedirect(venta.get_url_add_article_venta_ticket())

    if request.method == 'POST' and 'registrar_nuevo' in request.POST:
        return redirect('../add_new_cliente')

    if request.method == 'POST' and 'corte_ventas' in request.POST:
        return redirect('../corte_ventas')

    context = {
        "title": 'Ventas.',
        "form": nombre_tienda,
    }

    return render(request, "ventas.html", context)


def corte_ventas(request):
    '''
    >>> obj = control_venta.objects.filter(registrado__contains="2020-05-15")
    >>> for x in obj:
    ...   print(x.registrado)
    '''

    user = request.user
    form = corte_select_userForm(request.POST or None, request.FILES or None)
    #======================== LIQUIDACION ============================
    fecha = datetime.now()
    logging.critical("Fecha1: %s" % fecha)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++
    forma = "%B %d, %Y"
    select_date_time = fecha
    select_america_date_time = select_date_time.astimezone(timezone('America/Mexico_City'))
    select_date_time = str(select_date_time.strftime(forma))
    select_america_date_time = str(select_america_date_time.strftime(forma))
    fecha_hoy = select_america_date_time
    obj_liquidacion = None

    if liquidaciones_de_venta.objects.filter(usuario=user):
        liquidacion = liquidaciones_de_venta.objects.filter(usuario=user)
        for x in liquidacion:
            register_date_time = x.registrado
            register_date_time_america = register_date_time.astimezone(timezone('America/Mexico_City'))
            register_date_time = str(register_date_time.strftime(forma))
            register_date_time_america = str(register_date_time_america.strftime(forma))
            fecha_registrada = register_date_time_america
            logging.critical("Fecha3: %s" % register_date_time_america)

            if fecha_registrada == fecha_hoy:
                obj_liquidacion = liquidaciones_de_venta.objects.get(pk=x.pk)
            '''else:
                obj_liquidacion = None

    if obj_liquidacion == None:
        logging.critical("no existe")
        obj_liquidacion = 0
'''
        logging.critical("objeto: %s" % obj_liquidacion)

    if request.method == 'POST' and 'busca_usuario_fecha' in request.POST:
        if form.is_valid():
            lista = control_venta.objects.all()
            fecha = form.cleaned_data['fecha_pago']
            usuario = form.cleaned_data['usuario']
            logging.critical("Usuario a Consultar: %s" % usuario)
            logging.critical("Fecha1: %s" % fecha)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++
            forma = "%B %d, %Y"
            select_date_time = fecha
            select_america_date_time = select_date_time.astimezone(timezone('America/Mexico_City'))
            select_date_time = str(select_date_time.strftime(forma))
            select_america_date_time = str(select_america_date_time.strftime(forma))
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
            logging.critical("Fecha2: %s" % select_america_date_time)
            lista_tickets = []

            for x in lista:
                forma = "%B %d, %Y"
                register_date_time = x.registrado
                register_date_time_america = register_date_time.astimezone(timezone('America/Mexico_City'))
                register_date_time = str(register_date_time.strftime(forma))
                register_date_time_america = str(register_date_time_america.strftime(forma))
                logging.critical("Fecha3: %s" % register_date_time_america)
                if register_date_time_america == select_america_date_time and x.usuario == usuario:
                    logging.critical("+++++++++++++++++++++++++Venta Fecha Validada++++++++++++++++++++++++++++++")
                    logging.critical(
                        "Registro: %s, Realizado en la fecha de Venta Fecha: %s" % (x.pk, register_date_time_america))
                    logging.critical("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    lista_tickets.append(x.pk)

            total_corte = 0
            for i in lista_tickets:
              v1 = control_venta.objects.get(pk=i)

              '''if control_venta.objects.filter(pk=i, total_unidades_vendidas__lte=0):
              if inventario_store.objects.filter(articulo_id=a, unidades_vendidas__lte=0):
                  total_unidades_vendidas = objeto.unidades_vendidas + art_dicc[a]

                  logging.critical("Unidades Vendidas: %s" % total_unidades_vendidas)
              elif inventario_store.objects.filter(articulo_id=a, unidades_vendidas__gte=0):
                  total_unidades_vendidas = objeto.unidades_vendidas + art_dicc[a]
              else:
                  total_unidades_vendidas = art_dicc[a]
                  logging.critical("No tiene unidades vendidas: %s" % total_unidades_vendidas)'''

              ticket_total = v1.total
              logging.critical("valor prueba: %s" % ticket_total)
              total_corte = total_corte + ticket_total
              logging.critical("El valor de la suma es: %s" % total_corte)

            logging.critical("La Suma Global de el Corte es de: %s" % total_corte)
            if liquidaciones_de_venta.objects.filter(usuario=usuario):
                liquidacion = liquidaciones_de_venta.objects.filter(usuario=usuario)
                for x in liquidacion:
                    register_date_time = x.registrado
                    register_date_time_america = register_date_time.astimezone(timezone('America/Mexico_City'))
                    register_date_time = str(register_date_time.strftime(forma))
                    register_date_time_america = str(register_date_time_america.strftime(forma))
                    fecha_registrada = register_date_time_america
                    logging.critical("Fecha3: %s" % register_date_time_america)

                    if fecha_registrada == fecha_hoy:
                        obj_liquidacion = liquidaciones_de_venta.objects.get(pk=x.pk)
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            context = {
                "title": 'Ventas del Dia.',
                "lista": lista,
                "lista_tickets": lista_tickets,
                "usuario": user,
                "d_liquidar": total_corte,
                "liquidacion": obj_liquidacion,
            }
            return render(request, "Corte_Ventas.html", context)

    if request.method == 'POST' and 'Liquidar' in request.POST:
        logging.critical("Entro en liquidacion")
        lista = control_venta.objects.all()
        user = request.user
        liquidacion = request.POST['liquidacion']
        liquidacion_dia = int(liquidacion)
        logging.critical("Monto de Liquidacion: %s" % liquidacion_dia)
        valores = liquidaciones_de_venta(usuario=user, liquido=liquidacion_dia)
        valores.save()

        logging.critical("indice_registro: %s" % valores.pk)
        valores = get_object_or_404(liquidaciones_de_venta, pk=valores.pk)
        '''valores.monto_a_liquidar = liquidacion_dia
        #registro.balance = -10
        valores.save()'''

        #fecha = date.today()
        fecha = datetime.now()
        logging.critical("Fecha1: %s" % fecha)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++
        forma = "%B %d, %Y"
        select_date_time = fecha
        select_america_date_time = select_date_time.astimezone(timezone('America/Mexico_City'))
        select_date_time = str(select_date_time.strftime(forma))
        select_america_date_time = str(select_america_date_time.strftime(forma))
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++
        logging.critical("Fecha2: %s" % select_america_date_time)
        lista_tickets = []

        for x in lista:
            logging.critical("Flag1")
            forma = "%B %d, %Y"
            register_date_time = x.registrado
            register_date_time_america = register_date_time.astimezone(timezone('America/Mexico_City'))
            register_date_time = str(register_date_time.strftime(forma))
            register_date_time_america = str(register_date_time_america.strftime(forma))
            logging.critical("Fecha3: %s" % register_date_time_america)

            if register_date_time_america == select_america_date_time:
                usuario1 = str(user)
                usuario2 = str(x.usuario)
                if usuario1 == usuario2:
                    logging.critical("llegamos al usuario!!!")
                    logging.critical("+++++++++++++++++++++++++Venta Fecha Validada++++++++++++++++++++++++++++++")
                    logging.critical(
                        "Registro: %s, Realizado en la fecha de Venta Fecha: %s" % (x.pk, register_date_time_america))
                    logging.critical("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    lista_tickets.append(x.pk)

            '''if register_date_time_america == select_america_date_time and x.usuario == user:
                logging.critical("Flag2")
                logging.critical("+++++++++++++++++++++++++Venta Fecha Validada++++++++++++++++++++++++++++++")
                logging.critical(
                    "Registro: %s, Realizado en la fecha de Venta Fecha: %s" % (x.pk, register_date_time_america))
                logging.critical("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                lista_tickets.append(x.pk)'''

        total_corte = 0
        for i in lista_tickets:
            v1 = control_venta.objects.get(pk=i)
            ticket_total = v1.total
            logging.critical("valor prueba: %s" % ticket_total)
            total_corte = total_corte + ticket_total
            logging.critical("El valor de la suma es: %s" % total_corte)

        valores.monto_a_liquidar = total_corte
        balance = liquidacion_dia - total_corte
        valores.balance = balance
        valores.save()
        return redirect('../corte_ventas')

    context = {
        "title": 'Selecciona Usuario y Fecha.',
        "form": form,
        "usuario": user,
        "liquidacion": obj_liquidacion,
    }
    return render(request, "Corte_Ventas.html", context)


def add_articles_view(request, pk=None):
    cv = get_object_or_404(control_venta, pk=pk)
    query_list = inventario_store.objects.all().order_by('-pk')  # Trae los Articulos del Inventario
    user = request.user

    logging.critical("Folio de Control de Venta: %s" % cv)

    # =============Tabla de Inventario ========================================
    paginator = Paginator(query_list, 200)
    page_request_var = "historic"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    #=====================================================

    '''
    Comienza El Carrito de Compras para mandar los articulos de la tienda al carrito.
    '''
    if cv.clienteid == 1:
        flag_01 = 'SYSTEM'
        logging.critical("El USUARIO ES SYSTEM!!!")
    else:
        flag_01 = 'apartados'
        logging.critical("NO ES EL USUARIO SYSTEM!!!")

    product_list = inventario_store.objects.all()
    add_article = add_articles_Form(request.POST or None, request.FILES or None)
    pago_form = pago_con_Form(request.POST or None, request.FILES or None)
    encabezado = 'Agregar Articulos al Folio: %s, Cliente: %s' % (cv.pk, cv.cliente)

    '''
    Recibiendo articulos de la Tienda al Carrito de Compras.
    '''
    if request.method == 'POST' and 'Agregar' in request.POST:
        articulo_index = request.POST.get('indice')
        #nombre_art = request.POST.get('indice')
        cantidad_art = request.POST['valor']
        cantidad_art = int(cantidad_art)
        logging.critical("#====================== 1 ============================")
        logging.critical("Folio de Control de Venta: %s" % cv.pk)
        logging.critical("Nombre del Cliente: %s" % cv.cliente)
        logging.critical("#====================== 2 ============================")
        logging.critical("PK del Articulo: %s" % articulo_index)
        logging.critical("Cantidad: %s" % cantidad_art)
        logging.critical("Nombre: %s" % articulo_index)

        if inventario_store.objects.get(pk=articulo_index):
            articulo = inventario_store.objects.get(pk=articulo_index)
            logging.critical("Precio: $%s" % articulo.precio_venta)
            logging.critical("Nombre: %s" % articulo.nombre)
            logging.critical("Existencia: %s" % articulo.inventario)
            logging.critical("Articulo ID: %s" % articulo.articulo_id)

            if venta.objects.filter(id_venta=cv.pk, articulo_id=articulo.articulo_id):
                cantidad = venta.objects.filter(id_venta=cv.pk, articulo_id=articulo.articulo_id)
                logging.critical("Cantidad: %s" % cantidad)
                cantidad_articulos = len(cantidad)
                logging.critical("Cantidad del mismo articulo: %s" % cantidad_articulos)
            else:
                cantidad_articulos = 0

            if cantidad_art > articulo.inventario:
                logging.critical("Funciono!!: %s" % articulo.inventario)
                logging.critical("SOLO QUEDAN EN EXISTENCIA!!: %s" % articulo.inventario)
                '''messages.warning(request, "<center><a href='#'>SOLO QUEDAN EN EXISTENCIA: %s</a></center> Updated" % articulo.inventario,
                                 extra_tags='html_safe')
                                 '''
            else:
                logging.critical("SI HAY SUFICIENTES ARTICULOS PARA SURTIR ESTE PEDIDO!!!")

            # Contar cuantos articulos estan en el mismo ticket.
            v1 = venta.objects.filter(id_venta=cv.pk)
            cuenta = len(v1)
            logging.critical("Cuenta Total de Articulos en el mismo Ticket: %s" % cuenta)

            if cuenta == 0:
                logging.critical("========= Fase 1 conteo = 0 no hay ningun articulo en este folio ================")
                #instancia = add_article.save(commit=False)
                # instancia.save()
                # REALIZAR OPERACIONES
                logging.critical("ID venta: %s" % cv.pk)
                logging.critical("Nombre: %s" % articulo.nombre)
                logging.critical("ID articulo: %s" % articulo.articulo_id)
                logging.critical("Cantidad articulo: %s" % cantidad_art)
                logging.critical("Articulo precio venta: %s" % articulo.precio_venta)

                total_x_articulo = articulo.precio_venta * cantidad_art

                logging.critical("Total: %s" % total_x_articulo)
                logging.critical("Usuario: %s" % user)
                #logging.critical("Cantidad articulo: %s" % )

                registro = venta(id_venta=cv.pk, producto=articulo.nombre, articulo_id=articulo.articulo_id, cantidad=cantidad_art, precio=articulo.precio_venta, total=total_x_articulo, usuario=user)
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
                    registro = venta(id_venta=cv.pk, producto=articulo.nombre, articulo_id=articulo.articulo_id,
                                     cantidad=cantidad_art, precio=articulo.precio_venta, total=total_x_articulo,
                                     usuario=user)
                    registro.save()
                    logging.critical(
                        "========= Termina Fase 4 Folio: %s ================")
        lista_venta = venta.objects.filter(id_venta=cv.pk)
        cuenta_lista_venta = len(lista_venta)
        logging.critical("El Conteo de los Articulos de la Lista de Venta es de: %s" % cuenta_lista_venta)

        if cuenta_lista_venta > 0:
            imagen = articulo.imagen
            totales_lista = []
            for x in venta.objects.filter(id_venta=cv.pk):
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
                "object_list": queryset,
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
        "product_list": product_list,
        "object_list": queryset,
        # "queryset": lista_venta,
        # 'total': gran_total,
        # 'imagen': img,
    }
    return render(request, "ventas_add_articles.html", context)


def pago_contado(request, pk=None):
    cv = get_object_or_404(control_venta, pk=pk)
    user = request.user

    pago_form = pago_con_Form(request.POST or None, request.FILES or None)
    lista_venta = venta.objects.filter(id_venta=cv.pk)
    cuenta_lista_venta = len(lista_venta)
    logging.critical("El Conteo de Lista Venta es de: %s" % cuenta_lista_venta)

    if cuenta_lista_venta > 0:
        # imagen = articulo.imagen
        totales_lista = []
        art_dicc = {}

        for x in venta.objects.filter(id_venta=cv.pk):
            totales_lista.append(x.total)
            art_dicc[x.articulo_id] = x.cantidad

        logging.critical("Imprimiento diccionatio: %s" % art_dicc)
        logging.critical("voy a imprimir los articulos")
        for a in art_dicc:
            logging.critical("Imprimiento valor del diccionatio: %s ==> %s" % (a, art_dicc[a]))

        gran_total = 0
        for i in totales_lista:
            gran_total = gran_total + i

        # Registrando el Total de la cuenta en la DB en la tabla de Control de Ventas.
        # total_registro = control_venta.objects.get(pk=pk)
        cv.total = gran_total
        cv.save()
        logging.critical("El Gran TOTAL es : %s", gran_total)

        if request.method == 'POST' and 'cobrar' in request.POST:
            if pago_form.is_valid():
                ingreso = pago_form.cleaned_data['pago_con']
                logging.critical("Se resivio la cantidad de: %s" % ingreso)
                ingreso = int(ingreso)
                gran_total = int(gran_total)
                cv.pago_con = ingreso
                cv.status = 'Liquidado'
                time = datetime.now().date()
                cv.fecha_pago = time
                cv.save()
                # ++++++++++++++++++++ Descuento del Inventario Articulos ++++++++++++++++++++++
                for a in art_dicc:
                    logging.critical("Imprimiento valor del diccionatio: %s ==> %s" % (a, art_dicc[a]))

                    objeto = inventario_store.objects.get(articulo_id=a)
                    logging.critical(
                        "Imprimiendo el ID del articulo: %s, existencia: %s" % (objeto.articulo_id, objeto.inventario))

                    balance = objeto.inventario - art_dicc[a]

                    logging.critical("El total de articulos en existencia debe ser: %s" % balance)

                    objeto.inventario = balance

                    if inventario_store.objects.filter(articulo_id=a, unidades_vendidas__lte=0):
                        total_unidades_vendidas = objeto.unidades_vendidas + art_dicc[a]

                        logging.critical("Unidades Vendidas: %s" % total_unidades_vendidas)
                    elif inventario_store.objects.filter(articulo_id=a, unidades_vendidas__gte=0):
                        total_unidades_vendidas = objeto.unidades_vendidas + art_dicc[a]
                    else:
                        total_unidades_vendidas = art_dicc[a]
                        logging.critical("No tiene unidades vendidas: %s" % total_unidades_vendidas)



                    #total_unidades_vendidas = objeto.unidades_vendidas + art_dicc[a]
                    objeto.unidades_vendidas = total_unidades_vendidas
                    objeto.save()

                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if ingreso > gran_total:
                    cambio = ingreso - gran_total
                    logging.critical("Se debe regresar: %s" % cambio)
                else:
                    monto = ingreso - gran_total
                    cambio = ('ERROR!! Falta %s para saldar.' % monto)

                context = {
                    "title": 'Pago Contado.',
                    # "form": add_article,
                    "queryset": lista_venta,
                    'total': gran_total,
                    # 'imagen': imagen,
                    # 'pago_form': pago_form,
                    "pago_con": ingreso,
                    "cambio": cambio,
                }
                return render(request, "pago_contado.html", context)

        if request.method == 'POST' and 'terminar' in request.POST:
            return redirect('../../inventario&Store&0_1')

        context = {
            "title": 'Pago Contado.',
            # "form": add_article,
            "queryset": lista_venta,
            'total': gran_total,
            # 'imagen': imagen,
            'pago_form': pago_form,
        }
        return render(request, "pago_contado.html", context)


def pago_apartado(request, pk=None):
    cv = get_object_or_404(control_venta, pk=pk)
    lista_venta = venta.objects.filter(id_venta=cv)
    user = request.user
    pago_form = a_cuenta_Form(request.POST or None, request.FILES or None)

    cuenta_lista_venta = len(lista_venta)
    logging.critical("El Conteo de Lista Venta es de: %s" % cuenta_lista_venta)

    if cuenta_lista_venta > 0:
        totales_lista = []
        art_dicc = {}

        for x in venta.objects.filter(id_venta=cv):
            totales_lista.append(x.total)
            art_dicc[x.articulo_id] = x.cantidad

        logging.critical("Imprimiento diccionatio: %s" % art_dicc)
        logging.critical("voy a imprimir los articulos")

        for a in art_dicc:
            logging.critical("Imprimiento valor del diccionatio: %s ==> %s" % (a, art_dicc[a]))

        gran_total = 0
        for i in totales_lista:
            gran_total = gran_total + i

        # Registrando el Total de la cuenta en la DB en la tabla de Control de Ventas.
        # total_registro = control_venta.objects.get(pk=pk)
        cv.total = gran_total
        cv.save()
        deuda = cv.deve
        abonado = cv.a_cuenta
        logging.critical("El Gran TOTAL es : %s", gran_total)
        logging.critical("Se Deve: %s", deuda)
        logging.critical("Se lleva abonado: %s", abonado)

        if request.method == 'POST' and 'abonar' in request.POST:
            if pago_form.is_valid():
                ingreso = pago_form.cleaned_data['a_cuenta']
                logging.critical("Se resivio la cantidad de: %s" % ingreso)
                ingreso = int(ingreso)
                gran_total = int(gran_total)

                if not cv.a_cuenta:
                    acuenta = ingreso
                    logging.critical("si identifica el error!!")
                else:
                    acuenta = cv.a_cuenta + ingreso

                logging.critical("A cuenta: %s" % cv.a_cuenta)

                saldo = gran_total - acuenta
                cv.a_cuenta = acuenta
                # +++++++++++++++++++++++++++++
                if ingreso < gran_total:
                    if cv.deve:
                        if ingreso < cv.deve:
                            estado = 'Apartado'
                            resta = gran_total - acuenta
                            logging.critical("Se resta: %s, para Liquidar!" % resta)
                            cv.deve = resta
                            cv.save()
                    else:
                        estado = 'Apartado'
                        resta = gran_total - acuenta
                        logging.critical("Se resta: %s, para Liquidar!" % resta)
                        cv.deve = resta
                        cv.save()

                elif ingreso == cv.deve:
                    estado = 'Liquidado'
                    resta = gran_total - acuenta
                    logging.critical("Se resta: %s, para Liquidar!" % resta)
                    cv.deve = resta
                    cv.save()
                else:
                    estado = 'Liquidado'
                    monto = ingreso - gran_total
                    resta = ('ERROR!! Debemos Regresar %s para saldar. ya se liquido!' % monto)
                # +++++++++++++++++++++++++++++
                cv.status = estado
                cv.save()
                # +++++++++++++++++++ Registrar los Abonos ++++++++++++++++++++++
                abono = abonos_apartado(control_venta_id=pk, id_cliente=cv.clienteid, nombre_cliente=cv.cliente,
                                        total=gran_total, saldo=saldo, abono=ingreso)
                abono.save()
                # ++++++++++++++++++++ Descuento del Inventario Articulos ++++++++++++++++++++++
                for a in art_dicc:
                    logging.critical("Imprimiento valor del diccionatio: %s ==> %s" % (a, art_dicc[a]))

                    objeto = inventario_global.objects.get(articulo_id=a)
                    logging.critical(
                        "Imprimiendo el ID del articulo: %s, existencia: %s" % (objeto.articulo_id, objeto.existencia))
                    balance = objeto.existencia - art_dicc[a]
                    logging.critical("El total de articulos en existencia debe ser: %s" % balance)
                    objeto.existencia = balance
                    objeto.save()

                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                context = {
                    "title": 'Pago Contado.',
                    # "form": add_article,
                    "queryset": lista_venta,
                    'total': gran_total,
                    # 'imagen': imagen,
                    # 'pago_form': pago_form,
                    "pago_con": ingreso,
                    "deve": resta,
                    'saldo': cv.a_cuenta,
                }
                return render(request, "pago_apartado.html", context)

        if request.method == 'POST' and 'terminar' in request.POST:
            '''Imprime Ticket'''

            return redirect('../../inventario')

        context = {
            "title": 'Pago Contado.',
            # "form": add_article,
            "queryset": lista_venta,
            'total': gran_total,
            'saldo': cv.a_cuenta,
            # 'imagen': imagen,
            'pago_form': pago_form,
        }
        return render(request, "pago_apartado.html", context)


# ++++++++++++++++++++++++++++++++++
def create_ticket(request, pk=None):
    cv = get_object_or_404(control_venta, pk=pk)
    user = request.user
    ingreso = cv.pago_con
    # pago_form = pago_con_Form(request.POST or None, request.FILES or None)
    lista_venta = venta.objects.filter(id_venta=cv)
    cuenta_lista_venta = len(lista_venta)
    logging.critical("El Conteo de Lista Venta es de: %s" % cuenta_lista_venta)

    if cuenta_lista_venta > 0:
        # imagen = articulo.imagen
        totales_lista = []
        for x in venta.objects.filter(id_venta=cv):
            totales_lista.append(x.total)

        gran_total = 0
        for i in totales_lista:
            gran_total = gran_total + i

    cambio = cv.pago_con - gran_total

    context = {
        "title": 'Pago Contado.',
        # "form": add_article,
        "queryset": lista_venta,
        'total': gran_total,
        # 'imagen': imagen,
        # 'pago_form': pago_form,
        "pago_con": ingreso,
        "cambio": cambio,
    }
    return render(request, "ticket_print.html", context)


def clientes_view(request):
    query_list = cliente.objects.all().order_by('-pk')
    paginator = Paginator(query_list, 10)
    page_request_var = "historic"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": 'Lista Clientes.',
        "object_list": queryset,
        "page_request_var": page_request_var,
        # "imgbarcode" : filename,
        # "name": 'ean13.png',
    }
    return render(request, "clientes.html", context)


def cliente_detalle_view(request, pk=None):
    objeto = get_object_or_404(cliente, pk=pk)
    # ventas = get_object_or_404(control_venta, cliente=objeto.nombre)
    logging.critical("el pk del cliente es: %s" % pk)

    # ventas = get_object_or_404(control_venta, clienteid=pk)
    ventas = control_venta.objects.filter(clienteid=pk)

    totales_lista = []
    for x in ventas:
        logging.critical("deve: %s" % x.deve)
        totales_lista.append(x.deve)
        logging.critical("No Ticket:%s " % x.pk)

    gran_total = 0
    for i in totales_lista:
        gran_total = gran_total + i

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    logging.critical("total: %s" % gran_total)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # logging.critical("Ventas del Cliente: %s" % ventas)
    title = ("Perfil del Cliente %s" % objeto.nombre)

    context = {
        "title": title,
        "objeto": objeto,
        "tickets": ventas,
        "total": gran_total,
    }
    return render(request, "cliente_detalles.html", context)