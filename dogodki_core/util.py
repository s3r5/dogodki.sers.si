import urllib.request

def parse_saml_contact(string: str) -> dict:
	name, email = string.split("<")
	name = name.strip()
	email = email.rstrip(">")
	return {
		"givenName": name,
		"emailAddress": email
	}

ARNES_CERT_URL = "http://ds.aai.arnes.si/metadata/arnesaai-metadata-signing.crt"
def get_arnes_cert() -> str:
	resp = urllib.request.urlopen(ARNES_CERT_URL).read()
	return resp.decode("utf-8")
