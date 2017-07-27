from django.conf.urls import url,include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$',views.common_home,name='common_home'),    
    url(r'^users',views.member_home,name='member_home'),
    url(r'^login/',views.login_view,name='login'),
    url(r'^logout/',views.logout_view,name='logout'),
    url(r'^register/',views.register_view,name='register'),
    url(r'^first_page/',views.seperate_view,name='seperate'),


	url(r'^project/add/$',views.post_new,name='post_new'),
	url(r'^project/(?P<pk>\d+)/edit/$',views.post_edit,name='post_edit'),
	url(r'^project/(?P<pk>\d+)/delete/$',views.post_delete,name='post_delete'),

	url(r'^controller/login/',views.admin_login,name="admin_login"),
	url(r'^permission/(?P<pk>\d+)/',views.permission_member,name='permission_member'),
]
