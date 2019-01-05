from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import inlineformset_factory, modelform_factory
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from dogodki_app import models
from dogodki_app.util import FormsetMixin

# Create your views here.

class DashboardView(TemplateView):
	template_name = "dogodki/dashboard.html"

class DogodekView(DetailView):
	template_name = "dogodki/dogodek.html"
	model = models.Dogodek

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context["povabilo"] = models.Povabilo.objects.get(dogodek=self.object, uporabnik=self.request.user)
		
		obj_skupine = []
		found = False
		for skupina in self.object.skupine.all():
			obj_skupina = {
				"naslov": skupina.naslov,
				"število_mest": skupina.število_mest,
				"število_prijavljenih": skupina.prijavljeni.count(),
				"prijavljeni": [],
				"moja": False
			}

			obj_skupina["polna"] = obj_skupina["število_mest"] - obj_skupina["število_prijavljenih"] < 1

			for prijava in skupina.prijavljeni.all():
				obj_prijava = {
					"uporabnik": prijava.uporabnik,
					"jaz": False
				}

				if not found and prijava.uporabnik == self.request.user:
					obj_prijava["jaz"] = True
					obj_skupina["moja"] = True
					found = True

				obj_skupina["prijavljeni"].append(obj_prijava)

			obj_skupine.append(obj_skupina)

		context["skupine"] = obj_skupine
		return context

class EditDogodekMixin(FormsetMixin, PermissionRequiredMixin):
	template_name = "dogodki/dogodek_edit.html"
	model = models.Dogodek

	form_class = modelform_factory(models.Dogodek, exclude=())
	formset_class = inlineformset_factory(models.Dogodek, models.Skupina, exclude=(), extra=0, min_num=1)

class UstvariDogodekView(EditDogodekMixin, CreateView):
	permission_required = "dogodek.can_create"

class UrediDogodekView(EditDogodekMixin, UpdateView):
	permission_required = "dogodek.can_create"
