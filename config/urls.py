from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from profiles.views import RegisterView, activate_user_view

from config import views
from .views import (
    IndexView,
    AboutView,
)

urlpatterns = [
	path('admin/', admin.site.urls),
    path('index',IndexView.as_view(), name='index'),
    path('about/',AboutView.as_view(),name='about'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    path('', include('project.urls')),
]