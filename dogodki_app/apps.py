from django.apps import AppConfig


class DogodkiConfig(AppConfig):
	name = 'dogodki_app'

	def ready(self):
		# Register signal receivers
		import dogodki_app.signals
