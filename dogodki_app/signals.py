from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.conf import settings

from social_django.utils import load_strategy
from requests_oauthlib import OAuth2Session

from .util import trenutni_oddelek

import logging

@receiver(user_logged_in)
def posodobi_oddelek(sender, user, **kwargs):
	"""Ko se uporabnik prijavi, posodobi oddelek iz Microsoft Graph"""
	
	if not user.social_auth.exists():
		return
	social = user.social_auth.get(provider="microsoft-graph")
	
	access_token = social.get_access_token(load_strategy())
	graph_client = OAuth2Session(settings.SOCIAL_AUTH_MICROSOFT_GRAPH_KEY, token=social.extra_data)

	API_BASE = "https://graph.microsoft.com/v1.0/"
	url = API_BASE + "me/people?$filter=scoredEmailAddresses/any(a:a/address eq '" + user.email + "')&$select=department"
	
	contact = graph_client.get(url).json()
	try:
		department = contact["value"][0]["department"]
	except:
		logging.error(contact)

	oddelek = trenutni_oddelek(department)
	user.oddelek = oddelek
	user.save()
