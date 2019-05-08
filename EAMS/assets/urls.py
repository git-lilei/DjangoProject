from django.conf.urls import url
from . import views
# from haystack.views import SearchView

app_name = 'assets'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(\d+)/$', views.detail, name='detail'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
