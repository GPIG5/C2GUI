from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'c2gui'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^send_search_coord$', views.send_search_coord, name='send_search_coord'),
    url(r'^get_all_regions_status$', views.get_all_regions_status,
name='get_all_regions_status'),
    url(r'^send_drone_data$', views.send_drone_data, name='send_drone_data'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
