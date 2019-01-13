from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.formats import base_formats

from .models import *

# Register your models here.

@admin.register(Dogodek)
class DogodekProfileAdmin(admin.ModelAdmin):
	pass

@admin.register(Skupina)
class SkupinaProfileAdmin(admin.ModelAdmin):
	pass

@admin.register(Povabilo)
class PovabiloProfileAdmin(admin.ModelAdmin):
	pass

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
