"""dogodki_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
import dogodki_app.views

urlpatterns = [
	path("", dogodki_app.views.DashboardView.as_view()),
	path('admin/', admin.site.urls),
]
