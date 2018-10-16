from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from dogodki_app import models

# Create your views here.

class DashboardView(TemplateView):
	template_name = "dogodki/dashboard.html"

class DogodekView(DetailView):
	template_name = "dogodki/dogodek.html"
	model = models.Dogodek

class UstvariDogodekView(TemplateView):  # TODO: CreateView
	template_name = "dogodki/dogodek_edit.html"
