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
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/(\d+)/$', views.edit, name='edit'),
    url(r'^del_asset/(\d+)/$', views.del_asset, name='del_asset'),
]
