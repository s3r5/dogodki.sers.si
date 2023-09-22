from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.forms import inlineformset_factory, modelform_factory, ModelForm, ValidationError
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from datetime import date

from . import models
from .forms import DogodekPrijavaForm
from .util import FormsetMixin


# Create your views here.

class ProfilView(DetailView):
	template_name = "dogodki/profil.html"

	def get_object(self, **kwargs):
		return self.request.user


@method_decorator(vary_on_cookie, name="dispatch")
class DashboardView(LoginRequiredMixin, TemplateView):
	template_name = "dogodki/dashboard.html"

	def get_context_data(self):
		povabila = models.Povabilo.objects.filter(uporabnik=self.request.user)
		# Spodnje zahteva PostgreSQL!
		if self.request.user.is_staff:
			povabila = models.Povabilo.objects.distinct("dogodek")
		# Možna alternativa? https://stackoverflow.com/a/49291760
		danes = date.today()
		return {
			"odprta_povabila": povabila.filter(dogodek__datum__gte=danes),
			"pretekla_povabila": povabila.filter(dogodek__datum__lt=danes)
		}


@method_decorator(vary_on_cookie, name="dispatch")
class DogodekView(LoginRequiredMixin, DetailView):
	template_name = "dogodki/dogodek.html"
	model = models.Dogodek

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		is_staff = self.request.user.is_staff
		context["is_staff"] = is_staff

		try:
			context["povabilo"] = models.Povabilo.objects.get(dogodek=self.object, uporabnik=self.request.user)
		except:
			if not is_staff:
				raise PermissionDenied()

		obj_skupine = []
		found = False
		for skupina in self.object.skupine.all():
			prijavljeni = \
				skupina.prijavljeni.all() if is_staff \
				else skupina.prijavljeni.filter(uporabnik__oddelek=self.request.user.oddelek).all()

			obj_skupina = {
				"pk": skupina.pk,
				"opis": skupina.opis,
				"naslov": skupina.naslov,
				"število_mest":  skupina.število_mest,
				"število_prijavljenih": prijavljeni.count(),
				"prijavljeni": [],
				"moja": False
			}

			obj_skupina["polna"] = obj_skupina["število_mest"] - obj_skupina["število_prijavljenih"] < 1

			for prijava in prijavljeni:
				obj_prijava = {
					"uporabnik": prijava.uporabnik,
					"oddelek": prijava.uporabnik.oddelek,
					"jaz": False
				}

				if not found and prijava.uporabnik == self.request.user:
					obj_prijava["jaz"] = True
					obj_skupina["moja"] = True
					found = True

				obj_skupina["prijavljeni"].append(obj_prijava)

			obj_skupine.append(obj_skupina)

		context["skupine"] = obj_skupine
		context["odprto"] = "povabilo" in context and context["povabilo"].dogodek.cas_prijave > timezone.now()
		context["poteklo"] = "povabilo" in context and context["povabilo"].dogodek.rok_prijave < timezone.now()

		context["zaprto"] = context["odprto"] or context["poteklo"]

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


class DogodekPrijavaView(LoginRequiredMixin, UpdateView):
	form_class = DogodekPrijavaForm

	def get_object(self):
		return models.Povabilo.objects.get(dogodek__pk=self.kwargs["pk"], uporabnik=self.request.user.pk)

	def get_success_url(self):
		return self.object.dogodek.get_absolute_url()

	def form_invalid(self, form):
		for error in form.errors.values():
			messages.add_message(self.request, messages.ERROR, error.as_text())
		return redirect(self.object.dogodek.get_absolute_url())
