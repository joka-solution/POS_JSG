from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from home.views import home_page
from usuario.views import create_user

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(('home.urls', 'home'), namespace='POS_Store')),
    url(r'^consoleAdmin/Create&User/$', create_user, name='create_user'),
    url(r'^Store/', include(('Store.urls', 'Store'), namespace='Store')),
    url(r'^Distribucion/', include(('distribucion.urls', 'distribucion'), namespace='distribucion')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
