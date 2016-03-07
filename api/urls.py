from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^v1/users/(?P<screen_name>[a-zA-Z0-9._]+)$', views.get_user, name="get_user"),
    url(r'^v1/users/(?P<screen_name>[a-zA-Z0-9._]+)/tweets$', views.get_tweets, name="get_tweets"),
    url(r'^test_cache', views.test_cache),
]
