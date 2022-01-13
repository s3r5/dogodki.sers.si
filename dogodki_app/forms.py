from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from dogodki_app import models


class DogodekPrijavaForm(ModelForm):

    def clean(self):
        if self.instance.dogodek.rok_prijave < timezone.now():
            raise ValidationError("Rok za prijavo je potekel!")

        return super().clean()

    class Meta:
        model = models.Povabilo
        exclude = ("uporabnik", "dogodek")
