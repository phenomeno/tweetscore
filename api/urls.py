from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^v1/users/(?P<screen_name>[a-zA-Z0-9._]+)/twitter_data$', views.twitter_data, name="twitter_data"),
]
