from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class SkupinaListFilter(admin.SimpleListFilter):
	title = "skupina"
	parameter_name = "skupina"

	def has_output(self):
		return True

	def lookups(self, request, model_admin: admin.ModelAdmin):
		skupine = Skupina.objects.all()
		if "dogodek__id__exact" in request.GET:
			skupine = skupine.filter(dogodek__id__exact=int(request.GET["dogodek__id__exact"]))
		return [("null", "Brez")] + [(skupina.pk, skupina) for skupina in skupine]

	def queryset(self, request, queryset):
		if self.value():
			if self.value() == "null":
				return queryset.filter(skupina__isnull=True)
			else:
				return queryset.filter(skupina__pk__exact=self.value())
		else:
			return queryset
