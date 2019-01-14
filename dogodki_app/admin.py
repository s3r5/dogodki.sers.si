from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect, reverse
from django.urls import path
from django.views.generic import FormView

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.formats import base_formats

from .models import *
from .admin_util import *


# TODO: Popravi, ko bo obstajala prava relacija
oddelki = lambda: ((oddelek, oddelek) for oddelek in User.objects.filter(oddelek__isnull=False).values_list("oddelek", flat=True).distinct())
class PovabiOddelkeForm(forms.Form):
	oddelki = forms.MultipleChoiceField(choices=oddelki, widget=forms.CheckboxSelectMultiple)

class AdminPovabiOddelkeView(FormView):
	template_name = "dogodki/admin/dogodek_povabi_oddelke.html"
	form_class = PovabiOddelkeForm
	admin_site = None  # Filled in by as_view()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(self.admin_site.each_context(self.request))
		context.update({
			"opts": Dogodek._meta,
			"dogodek": Dogodek.objects.get(pk=self.kwargs["pk"])
		})
		return context
	
	def form_valid(self, form):
		for user in User.objects.filter(oddelek__in=form.cleaned_data["oddelki"]):
			Povabilo.objects.get_or_create(dogodek_id=self.kwargs["pk"], uporabnik=user)
		return redirect(reverse("admin:dogodki_app_dogodek_change", args=[self.kwargs["pk"]]))

# Register your models here.

class SkupinaInline(admin.StackedInline):
	model = Skupina
	extra = 0

@admin.register(Dogodek)
class DogodekAdmin(admin.ModelAdmin):
	change_form_template = "dogodki/admin/dogodek.html"

	inlines = [
		SkupinaInline
	]

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			path('<int:pk>/povabi_oddelek/', self.admin_site.admin_view(AdminPovabiOddelkeView.as_view(admin_site=self.admin_site)), name="dogodki_app_povabi_oddelek"),
		]
		return my_urls + urls

@admin.register(Povabilo)
class PovabiloAdmin(admin.ModelAdmin):
	search_fields = ("uporabnik__first_name", "uporabnik__last_name", "uporabnik__username", "skupina__naslov", "uporabnik__oddelek")
	autocomplete_fields = ("uporabnik",)

	list_display = ("dogodek", "uporabnik", "skupina", "povabilo_oddelek")
	list_filter = ("uporabnik__oddelek", SkupinaListFilter, "dogodek")

	def povabilo_oddelek(self, povabilo):
		return povabilo.uporabnik.oddelek

	povabilo_oddelek.short_description = "oddelek"

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if obj:
			form.base_fields["skupina"].queryset = form.base_fields["skupina"].queryset.filter(dogodek=obj.dogodek)
		else:
			form.base_fields["skupina"].queryset = form.base_fields["skupina"].queryset.none()
		return form

# django-import-export
class UserResource(ModelResource):
	first_name = Field(attribute="first_name", column_name="Ime")
	last_name = Field(attribute="last_name", column_name="Priimek")
	email = Field(attribute="email", column_name="Email")
	oddelek = Field(attribute="oddelek", column_name="Oddelek")

	def before_import_row(self, row, **kwargs):
		row["username"] = row["Email"].split("@")[0]
		return row
	
	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "oddelek", "username")
		import_id_fields = ("email",)

@admin.register(User)
class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
	resource_class = UserResource
	formats = [base_formats.XLS]
	import_template_name = "dogodki/import.html"

CustomUserAdmin.fieldsets += ('Custom fields set', {'fields': ('oddelek',)}),
