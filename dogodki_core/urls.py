"""dogodki_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
import dogodki_app.views

urlpatterns = [
	path("", dogodki_app.views.DashboardView.as_view(), name="dashboard"),
	path("dogodek/ustvari", dogodki_app.views.UstvariDogodekView.as_view(), name="ustvari_dogodek"),
	path("dogodek/<int:id>", dogodki_app.views.DogodekView.as_view(), name="dogodek"),
	path('admin/', admin.site.urls),
]
