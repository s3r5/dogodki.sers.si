from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import inlineformset_factory, modelform_factory

from dogodki_app import models
from dogodki_app.util import FormsetMixin

# Create your views here.

class DashboardView(TemplateView):
	template_name = "dogodki/dashboard.html"

class DogodekView(DetailView):
	template_name = "dogodki/dogodek.html"
	model = models.Dogodek

class EditDogodekMixin(FormsetMixin):
	template_name = "dogodki/dogodek_edit.html"
	model = models.Dogodek

	form_class = modelform_factory(models.Dogodek, exclude=())
	formset_class = inlineformset_factory(models.Dogodek, models.Skupina, exclude=(), extra=0, min_num=1)

class UstvariDogodekView(EditDogodekMixin, CreateView):
	pass

class UrediDogodekView(EditDogodekMixin, UpdateView):
	pass
