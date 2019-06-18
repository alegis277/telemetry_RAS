from django.urls import path
from django.urls import include, re_path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.jpeg', permanent=True)

from . import views

urlpatterns = [
	path('favicon.ico', favicon_view, name='favicon'),
	path('', views.index, name='index'),

]