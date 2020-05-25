from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

# Register your models here.


class UserModelAdmin(admin.ModelAdmin):
    list_display = ["pk", "username", "first_name",  "last_name", "is_vendedor", "is_supervisor", "is_gerente", "is_patron"]
    list_display_links = ["username"]
    class Meta:
        model = User


admin.site.register(User, UserModelAdmin)