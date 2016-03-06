from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^', views.index, name='index'),
    url(r'^twitter_data\\?(?P<username>[a-zA-Z0-9._]+)$', views.twitter_data, name="twitter_data")
]
