from django.views.generic.base import TemplateView

# Create your views here.

class DashboardView(TemplateView):
	template_name = "dogodki/dashboard.html"

class DogodekView(TemplateView): # TODO: DetailView
	template_name = "dogodki/dogodek.html"

class UstvariDogodekView(TemplateView):  # TODO: CreateView
	template_name = "dogodki/dogodek_edit.html"
