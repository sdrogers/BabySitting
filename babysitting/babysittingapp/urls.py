from django.conf.urls import patterns,url
from babysittingapp import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^register/$',views.register,name="register"),
	url(r'^login/$',views.user_login,name="login"),
	url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^addactivity/$',views.add_activity,name='add_activity'),
	url(r'^viewactivity/$',views.view_activity,name='view_activity'),
	url(r'^editactivity/(?P<activity_id>\w+)/$',views.edit_activity,name='edit_activity'),
	url(r'^deleteactivity/(?P<activity_id>\w+)/$',views.delete_activity,name='edit_activity'),
	)