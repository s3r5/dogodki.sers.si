from django.db import models
from django.core.validators import MinValueValidator
from django.urls.base import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	oddelek = models.CharField(max_length=5, blank=True, null=True)
	
	def __str__(self):
		return self.first_name + " " + self.last_name

class Dogodek(models.Model):
	naslov = models.CharField(max_length=50)
	datum = models.DateField()
	rok_prijave = models.DateTimeField()
	opis = models.TextField(null=True, blank=False)

	@property
	def število_mest(self):
		# TODO: Optimizacija?
		return sum((skupina.število_mest for skupina in self.skupine.all()))

	@property
	def število_navoljo(self):
		# TODO: Optimizacija?
		return self.število_mest - sum((skupina.prijavljeni.count() for skupina in self.skupine.all()))

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
