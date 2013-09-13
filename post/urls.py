from django.conf.urls import patterns, url

urlpatterns = patterns('post.views',
	url(r'^add_post/$', 'add_post',      
		name="add_post"),
	url(r'^detail/(?P<slug>[\w-]+)/$', 'post_detail',      
		name="post_detail"),
	url(r'^user_posts/$', 'user_posts',      
		name="user_posts"),
 )
