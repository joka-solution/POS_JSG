from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .forms import create_userForm
from .models import User
# Create your views here.


def create_user(request):
#    if request.user.is_superuser:
    form = create_userForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and 'create_user' in request.POST:
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.is_vendedor == True and instance.is_gerente == False and instance.is_supervisor == False and instance.is_patron == False:
                User.objects.create_user(username=instance.username, first_name=instance.first_name,  last_name=instance.last_name, password=instance.password,  is_vendedor=True)
                messages.success(request, "Successfully Add User %s, with profile: vendedor." % instance.username )
            elif instance.is_vendedor == False and instance.is_gerente == True and instance.is_supervisor == False and instance.is_patron == False:
                User.objects.create_user(username=instance.username, first_name=instance.first_name,  last_name=instance.last_name, password=instance.password,  is_gerente=True)
                messages.success(request, "Successfully Add User %s, with profile: gerente." % instance.username )
            elif instance.is_vendedor == False and instance.is_gerente == False and instance.is_supervisor == True and instance.is_patron == False:
                User.objects.create_user(username=instance.username, first_name=instance.first_name,  last_name=instance.last_name, password=instance.password,  is_supervisor=True)
                messages.success(request, "Successfully Add User %s, with profile: supervisor." % instance.username )
            elif instance.is_vendedor == False and instance.is_gerente == False and instance.is_supervisor == False and instance.is_patron == True:                    
                User.objects.create_user(username=instance.username, first_name=instance.first_name,  last_name=instance.last_name, password=instance.password,  is_patron=True)
                messages.success(request, "Successfully Add User %s, with profile: patron." % instance.username )
            else:
                 messages.success(request,
                                     "<h3><span class='label label-danger'>Please only select one profile  to continue.</span></h3>",
                                     extra_tags='html_safe')                                    
            index = User.objects.filter(username=instance.username)
            return HttpResponseRedirect('/')
    context = {
        'form': form,
    }
    return render(request, "create_user.html", context)
