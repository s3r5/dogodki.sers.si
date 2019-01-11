from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

admin.site.register(User, UserAdmin)
UserAdmin.fieldsets += ("Šola", {'fields': ('oddelek',)}),

class SkupinaInline(admin.StackedInline):
	model = Skupina
	extra = 0

@admin.register(Dogodek)
class DogodekAdmin(admin.ModelAdmin):
	inlines = [
		SkupinaInline
	]
	
@admin.register(Povabilo)
class PovabiloAdmin(admin.ModelAdmin):
	pass
