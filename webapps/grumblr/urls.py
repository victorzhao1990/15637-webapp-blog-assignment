from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'grumblr.views.home', name='home'),
    url(r'^signup/$', 'grumblr.views.registration', name='registration'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'grumblr/login.html'}, name='login'),

    url(r'^profile/$', 'grumblr.views.profile', name='profile'),
    url(r'^profile-edit/$', 'grumblr.views.profile_edit', name='profile_edit'),
    url(r'^profile/(?P<username>[A-Za-z]\w*)/$', 'grumblr.views.profile', name='profile'),
    url(r'^globalstream/$', 'grumblr.views.home', name='globalstream'),
    url(r'^newPost/$', 'grumblr.views.new_post', name='new_post'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^photo/(?P<username>[A-Za-z]\w*)/$', 'grumblr.views.get_photo', name='photo'),
    url(r'^follower-stream/$', 'grumblr.views.follower_stream', name='follower_stream'),
    url(r'^follow/$', 'grumblr.views.follow', name='follow'),
    # Reset password
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'grumblr/registration/password_reset_form.html'}, name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'grumblr/registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'grumblr/registration/password_reset_confirm.html',
         'post_reset_redirect': '/grumblr/password/done/'}, name='password_reset_confirm'),
    url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'grumblr/registration/password_reset_complete.html'}, name='password_reset_complete'),
    # Ajax request for render the posts
    url(r'^get-posts$', 'grumblr.views.get_posts'),
    url(r'^get-posts/(?P<username>[A-Za-z]\w*)/(?P<log_id>\d+)$', 'grumblr.views.get_posts'),
    url(r'^get-posts/(?P<username>[A-Za-z]\w*)$', 'grumblr.views.get_posts'),

    url(r'^get-posts/(?P<log_id>\d+)$', 'grumblr.views.get_posts'),
    url(r'^get-changes$', 'grumblr.views.get_changes'),
    url(r'^get-changes/(?P<log_id>\d+)$', 'grumblr.views.get_changes'),
    url(r'^add-post', 'grumblr.views.add_post'),

    # Ajax request for render the comments
    url(r'^get-comments$', 'grumblr.views.get_comments'),
    url(r'^get-comments/(?P<post_id>\d+)$', 'grumblr.views.get_comments'),
    url(r'^get-comment-changes$', 'grumblr.views.get_comment_changes'),
    url(r'^get-comment-changes/(?P<post_id>\d+)/(?P<log_id>\d+)$', 'grumblr.views.get_comment_changes'),
    url(r'^add-comment/(?P<post_id>\d+)$', 'grumblr.views.add_comment'),

    url(r'^follower-list$', 'grumblr.views.follower_list'),

]
