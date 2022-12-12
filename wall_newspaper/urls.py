from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls') ),
    path('editorjs/', include('django_editorjs_fields.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403 = 'main.views.error_403'
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'