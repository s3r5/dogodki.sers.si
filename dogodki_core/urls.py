"""dogodki_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from dogodki_core import settings
import dogodki_app.views

urlpatterns = [
	path("", dogodki_app.views.DashboardView.as_view(), name="dashboard"),
	path("dogodek/ustvari", dogodki_app.views.UstvariDogodekView.as_view(), name="ustvari_dogodek"),
	path("dogodek/<int:pk>", dogodki_app.views.DogodekView.as_view(), name="dogodek"),
	path("prijava", auth_views.LoginView.as_view(), name='login'),
    path("odjava", auth_views.LogoutView.as_view(), name='logout'),
	path('admin/', admin.site.urls),
]

if settings.DEBUG:
	import debug_toolbar
	urlpatterns = [
		path('__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns
