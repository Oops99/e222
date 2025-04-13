from django.urls import path
from . import views
from django.views import static
from django.urls import re_path as url
from django.conf import settings

urlpatterns = [
    path('<int:song_id>.html', views.playview, name='play'),
    path('download/<int:song_id>.html', views.downloadview, name='download'),
    url('^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static')
]