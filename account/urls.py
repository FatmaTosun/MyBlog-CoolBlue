from django.conf.urls import patterns, url
from django.contrib.auth.views import (password_change, password_change_done,
                                       password_reset, password_reset_confirm,
                                       password_reset_done,
                                       password_reset_complete)


urlpatterns = patterns('account.views',
	url(r'^login/$', 'login_user',      
		name="login"),

	url(r'^registration/$', 'registration',      
		name="registration"),

  url(r'^confirm/$', 'confirm',      
    name="confirm"),

	url(r'^logout/$', 'logout_user',      
		name="logout"),

	url(r'^update_profile/$', 'update_profile', name="update_profile"),
 )
