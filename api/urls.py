from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^api/v1/users/(?P<screen_name>[a-zA-Z0-9._]+)$', views.get_user, name="get_user"),
    url(r'^api/v1/users/(?P<screen_name>[a-zA-Z0-9._]+)/tweets$', views.get_tweets, name="get_tweets"),
    url(r'^api/v1/users/(?P<screen_name>[a-zA-Z0-9._]+)/friends$', views.get_friends, name="get_friends"),
    url(r'^api/v1/users\\?(?P<user_id>[0-9]+)$', views.get_users, name="get_users"),
]
