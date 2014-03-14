from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
        url(r'^$', views.main, name='main_page'),
        url(r'^about/$', views.about, name='about'),
        url(r'^thirdpage/$', views.thirdpage, name='thirdpage'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
        url(r'^category/<category_name_url>/add_page/$', views.add_page, name='add_page'),)# New!