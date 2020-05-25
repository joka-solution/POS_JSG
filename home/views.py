from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login as log_in_user, logout as log_out_user
import logging

# Create your views here.

def home_page(request):
    """
    This is a home page for my site.
    """
    if request.method == 'POST' and 'login_user' in request.POST:
        logging.warning("precionaron boton login.")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                logging.warning("El usuario es valido.")
                logging.warning("El index del usuario es: %s" % user.pk)
                log_in_user(request, user)
                usuario = request.user.username
                logging.critical("Username: %s" % usuario)
                return HttpResponseRedirect("/")

    context = {
        "title": 'Welcome.'
    }

    return render(request, 'index.html', context)

def logout(request):
    log_out_user(request)
    return HttpResponseRedirect("/")