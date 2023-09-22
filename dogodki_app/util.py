from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic.edit import UpdateView

from .models import Povabilo


def get_username(strategy, details, backend, user=None, *args, **kwargs):
    if not user:
        username = details["email"].split("@")[0]
    else:
        username = strategy.storage.user.get_username(user)
    return {"username": username}


def pošlji_obvestila(dogodek, emails):
    email = EmailMessage(
        subject="Povabilo na dogodek: %s" % dogodek,
        body=render_to_string("dogodki/mail/vabilo.txt", {"dogodek": dogodek}),
        from_email=None,  # Use default
        to=[],
        bcc=emails
    )

    email.send()

    Povabilo.objects.filter(dogodek=dogodek, uporabnik__email__in=emails).update(email_poslan=True)


class FormsetMixin:
    object = None

    def get(self, request, *args, **kwargs):
        if isinstance(self, UpdateView):
            self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)

        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if isinstance(self, UpdateView):
            self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            "instance": self.object
        }
        if self.request.method == "POST":
            kwargs["data"] = self.request.POST
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
