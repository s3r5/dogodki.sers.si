"""dogodki_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

import dogodki_app.views
from dogodki_core import settings

urlpatterns = [
    path("", dogodki_app.views.DashboardView.as_view(), name="dashboard"),
    path("dogodek/ustvari", dogodki_app.views.UstvariDogodekView.as_view(), name="ustvari_dogodek"),
    path("dogodek/<int:pk>", dogodki_app.views.DogodekView.as_view(), name="dogodek"),
    path("dogodek/<int:pk>/uredi", dogodki_app.views.UrediDogodekView.as_view(), name="uredi_dogodek"),
    path("profil", dogodki_app.views.ProfilView.as_view(), name='profil'),
    path("dogodek/<int:pk>/prijava", dogodki_app.views.DogodekPrijavaView.as_view(), name="dogodek_prijava"),
    path("prijava", auth_views.LoginView.as_view(), name='login'),
    path("odjava", auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
