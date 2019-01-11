from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .admin_util import *

# Register your models here.

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += ("Šola", {'fields': ('oddelek',)}),

class SkupinaInline(admin.StackedInline):
	model = Skupina
	extra = 0

@admin.register(Dogodek)
class DogodekAdmin(admin.ModelAdmin):
	change_form_template = "dogodki/admin/dogodek.html"

	inlines = [
		SkupinaInline
	]

@admin.register(Povabilo)
class PovabiloAdmin(admin.ModelAdmin):
	search_fields = ("uporabnik__first_name", "uporabnik__last_name", "uporabnik__username", "skupina__naslov", "uporabnik__oddelek")
	autocomplete_fields = ("uporabnik",)

	list_display = ("dogodek", "uporabnik", "skupina", "povabilo_oddelek")
	list_filter = ("uporabnik__oddelek", SkupinaListFilter, "dogodek")

	def povabilo_oddelek(self, povabilo):
		print(povabilo.uporabnik.oddelek, povabilo, povabilo.uporabnik)
		return povabilo.uporabnik.oddelek

	povabilo_oddelek.short_description = "oddelek"

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if obj:
			form.base_fields["skupina"].queryset = form.base_fields["skupina"].queryset.filter(dogodek=obj.dogodek)
		else:
			form.base_fields["skupina"].queryset = form.base_fields["skupina"].queryset.none()
		return form
	
