from django.urls import re_path

from . import views


urlpatterns = [
	re_path(r'^purchase/(?P<filename>[^/]+)$', views.CustomerList.as_view()),
    re_path(r'^purchase/', views.CustomerList.as_view()),
]
