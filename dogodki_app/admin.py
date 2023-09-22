from django import forms
from django.contrib.auth.admin import UserAdmin
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import path
from django.views.generic import FormView
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.formats import base_formats
from import_export.resources import ModelResource

from .admin_util import *
from .util import pošlji_obvestila

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


class PovabiloResource(ModelResource):
    dogodek__naslov = Field(attribute="dogodek__naslov", column_name="Naslov dogodka")
    skupina__naslov = Field(attribute="skupina__naslov", column_name="Ime skupine")
    uporabnik__first_name = Field(attribute="uporabnik__first_name", column_name="Dijak - ime")
    uporabnik__last_name = Field(attribute="uporabnik__last_name", column_name="Dijak - priimek")
    uporabnik__oddelek = Field(attribute="uporabnik__oddelek", column_name="Dijak - oddelek")

    class Meta:
        model = Povabilo
        fields = (
            "dogodek__naslov", "skupina__naslov", "uporabnik__first_name", "uporabnik__last_name", "uporabnik__oddelek")


@admin.register(Povabilo)
class PovabiloAdmin(ImportExportModelAdmin):
    resource_class = PovabiloResource
    search_fields = (
        "uporabnik__first_name", "uporabnik__last_name", "uporabnik__username", "uporabnik__email", "skupina__naslov",
        "uporabnik__oddelek")
    autocomplete_fields = ("uporabnik",)

    list_display = ("dogodek", "uporabnik", "uporabnik_email", "skupina", "prijavljeni_od_celote", "povabilo_oddelek")
    list_filter = ("uporabnik__oddelek", SkupinaListFilter, "dogodek")

    def povabilo_oddelek(self, povabilo):
        return povabilo.uporabnik.oddelek

    def uporabnik_email(self, povabilo):
        return povabilo.uporabnik.email

    def prijavljeni_od_celote(self, povabilo):
        return f"{povabilo.skupina.prijavljeni.filter(uporabnik__oddelek=povabilo.uporabnik.oddelek).count()}/{povabilo.skupina.število_mest}" if (
                povabilo.skupina is not None) else "N/A"

    prijavljeni_od_celote.short_description = "Prijavljeni od skupine"

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

    list_display = ("username", "email", "first_name", "last_name", "is_staff", "oddelek")
    list_filter = ("oddelek", "is_staff", "is_superuser", "is_active")


CustomUserAdmin.fieldsets += ('Custom fields set', {'fields': ('oddelek',)}),


@admin.register(Obvestilo)
class ObvestiloAdmin(admin.ModelAdmin):
    filter_horizontal = ("skupine",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        obvestilo = Obvestilo.objects.get(id=form.instance.id)
        if (change is False or change is None) and obvestilo.email_poslan is False:
            emails = []

            for skupina in obvestilo.skupine.all():
                for prijavljen in skupina.prijavljeni.all():
                    emails.append(prijavljen.uporabnik.email)

            email = EmailMessage(
                subject=obvestilo.naslov,
                body=obvestilo.vsebina,
                from_email=None,
                to=[],
                bcc=list(dict.fromkeys(emails))
            )
            email.send()

            Obvestilo.objects.filter(id=form.instance.id).update(email_poslan=True)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["naslov", "skupine", "vsebina", "email_poslan"]
        return self.readonly_fields
