from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'c2gui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_search_coord$', views.send_search_coord, name='send_search_coord'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
