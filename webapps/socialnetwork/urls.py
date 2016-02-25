from django.conf.urls import url, include
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
	url(r'^$', auth_views.login, {'template_name' : 'socialnetwork/login.html'}, name = 'login'),
	url(r'^login$', auth_views.login, {'template_name' : 'socialnetwork/login.html'}, name = 'login'),
	url(r'^logout$', auth_views.logout_then_login, name = 'logout'),
	url(r'^photo/(?P<name>\w+)$', views.get_photo, name = 'photo'),
	url(r'^socialnetwork/edit_entry$', views.edit_entry, name = 'edit'),
	url(r'^socialnetwork/$', views.profile, name = 'profile'),
	url(r'^socialnetwork/register$', views.register, name = 'register'),
	url(r'^socialnetwork/global$', views.global_post, name = 'global_post'),
	url(r'^socialnetwork/profile$', views.profile, name = 'profile'),
	url(r'^socialnetwork/do_post$', views.do_post, name = 'do_post'),
	url(r'^socialnetwork/profile/(?P<name>\w+)$', views.other_profile, name = 'other_profile'),
	url(r'^socialnetwork/delete_post/(?P<id>\d+)$', views.delete_post, name = 'delete'),
	url(r'^socialnetwork/follow_users/(?P<name>\w+)$', views.follow_users, name = 'follow'),
	url(r'^socialnetwork/unfollow_users/(?P<name>\w+)$', views.follow_delete, name = 'unfollow'),
	url(r'^socialnetwork/follow$', views.follow_stream, name = 'follow_stream'),
	url(r'^socialnetwork/post_list$', views.post_list, name = 'post_list'),
	url(r'^socialnetwork/do_comment$', views.do_comment, name = 'do_comment'),
	url(r'^socialnetwork/comment_list/(?P<post_id>\d+)$', views.comment_list, name = 'comment_list'),
]