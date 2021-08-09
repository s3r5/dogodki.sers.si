from django import forms
from django.shortcuts import redirect
from django.urls import path
from django.views.generic import FormView
from django.db.models import Q

from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.formats import base_formats

from .util import pošlji_obvestila
from .admin_util import *

# TODO: Popravi, ko bo obstajala prava relacija
oddelki = lambda: ((oddelek, oddelek) for oddelek in
                   User.objects.filter(oddelek__isnull=False).values_list("oddelek", flat=True).distinct())


class PovabiOddelkeForm(forms.Form):
    oddelki = forms.MultipleChoiceField(choices=oddelki, widget=forms.CheckboxSelectMultiple)


class AdminPovabiOddelkeView(FormView):
    template_name = "dogodki/admin/dogodek_povabi_oddelke.html"
    form_class = PovabiOddelkeForm
    admin_site = None  # Filled in by as_view()

    def get_context_data(self, **kwargs):
        self.dogodek = Dogodek.objects.get(pk=self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        context.update(self.admin_site.each_context(self.request))
        context.update({
            "opts": Dogodek._meta,
            "dogodek": self.dogodek
        })
        return context

    def form_valid(self, form):
        self.dogodek = Dogodek.objects.get(pk=self.kwargs["pk"])
        users = User.objects.filter(oddelek__in=form.cleaned_data["oddelki"])

        emails = []

        for user in users:
            povabilo, created = Povabilo.objects.get_or_create(dogodek=self.dogodek, uporabnik=user)
            if not povabilo.email_poslan:
                emails.append(user.email)

        pošlji_obvestila(self.dogodek, emails)

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
            path('<int:pk>/povabi_oddelek/',
                 self.admin_site.admin_view(AdminPovabiOddelkeView.as_view(admin_site=self.admin_site)),
                 name="dogodki_app_povabi_oddelek"),
        ]
        return my_urls + urls


@admin.register(Povabilo)
class PovabiloAdmin(admin.ModelAdmin):
    search_fields = (
    "uporabnik__first_name", "uporabnik__last_name", "uporabnik__username", "skupina__naslov", "uporabnik__oddelek")
    autocomplete_fields = ("uporabnik",)

    list_display = ("dogodek", "uporabnik", "skupina", "povabilo_oddelek")
    list_filter = ("uporabnik__oddelek", SkupinaListFilter, "dogodek")

    def povabilo_oddelek(self, povabilo):
        return povabilo.uporabnik.oddelek

    povabilo_oddelek.short_description = "oddelek"
    povabilo_oddelek.admin_order_field = "uporabnik__oddelek"

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

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        email_col = dataset.headers.index("Email")

        # Iz uvožene datoteke odstrani vse vnose brez e-poštnega naslova
        to_delete = []
        for i, row in enumerate(dataset):
            if not "@" in row[email_col]:
                to_delete.append(i)
        for i in to_delete:
            del dataset[i]

    def before_import_row(self, row, **kwargs):
        row["username"] = row["Email"].split("@")[0]
        row["fresh"] = True

        return row

    # def for_delete(self, row, instance):
    #     if row["fresh"]:
    #         return False
    #     return True

    # def after_import_row(self, row, row_result, **kwargs):
    #     row["fresh"] = True

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if dry_run:
            return
        # Ne odstrani administratorjav oz. staff-a
        User.objects.filter(fresh=False, is_staff=False).delete()
        # Spremeni vse "frišne" uporabnike v "stare"
        User.objects.filter(fresh=True).update(fresh=False)

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
