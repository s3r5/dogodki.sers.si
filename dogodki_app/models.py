from django.db import models
from django.core.validators import MinValueValidator
from django.urls.base import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	pass

class Dogodek(models.Model):
	naslov = models.CharField(max_length=50)
	datum = models.DateField()
	rok_prijave = models.DateTimeField()
	opis = models.TextField(null=True, blank=False)

	def prijavljeni(self):
		return self.povabljeni.exclude(skupina__isnull=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["prijavljeni"] = self.prijavljeni()
		return context

	class Meta:
		verbose_name = "Dogodek"
		verbose_name_plural = "Dogodki"

	def __str__(self):
		return self.naslov

	def get_absolute_url(self):
		return reverse("dogodek", kwargs={"pk": self.pk})

class Skupina(models.Model):
	naslov = models.CharField(max_length=50)
	opis = models.TextField(null=True, blank=False)
	število_mest = models.PositiveIntegerField(validators=[MinValueValidator(1)])

	dogodek = models.ForeignKey(Dogodek, on_delete=models.CASCADE, related_name="skupine")

	class Meta:
		verbose_name = "Skupina"
		verbose_name_plural = "Skupine"

	def __str__(self):
		return "%s: %s" % (self.dogodek, self.naslov)

class Povabilo(models.Model):
	uporabnik = models.ForeignKey(User, on_delete=models.CASCADE)
	skupina = models.ForeignKey(Skupina, blank=True, null=True, related_name="prijavljeni", on_delete=models.CASCADE)

	dogodek = models.ForeignKey(Dogodek, on_delete=models.CASCADE, related_name="povabljeni")

	class Meta:
		verbose_name = "Povabilo"
		verbose_name_plural = "Povabila"

	def __str__(self):
		return "%s: %s (%s)" % (self.dogodek, self.uporabnik, self.skupina)
