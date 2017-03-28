from django.conf.urls import url

from . import views

app_name = 'recommend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_recommendations/$', views.get_recommendations, name='get_recommendations'),
    url(r'^get_recommendations/(?P<steam_id>[0-9]{17})/$', views.get_recommendations, name='get_recommendations')
]