"""
Django settings for dogodki_django project.
"""
import os

import environ

##################
#                #
#   APP CONFIG   #
#                #
##################

INSTALLED_APPS = [
	"dogodki_app",

	"import_export",

	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
]

MIDDLEWARE = [
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

# URLs
ROOT_URLCONF = 'dogodki_core.urls'

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

WSGI_APPLICATION = 'dogodki_core.wsgi.application'

#######################
#                     #
#   INSTANCE CONFIG   #
#                     #
#######################

root = environ.Path(__file__) - 2

# Fetch env vars
os.environ.setdefault("ENV_FILE", root(".env"))
env = environ.Env(
	DEBUG=(bool, False),
	DEBUG_IPS=(list, []),
	ALLOWED_HOSTS=(list, []),
	ADMINS=(list, ["admin"])
)
if os.path.isfile(os.environ["ENV_FILE"]):
	env.read_env(os.environ["ENV_FILE"])

# File storage
STATIC_ROOT = root(env("STATIC_DIR", default="../static"))
MEDIA_ROOT = root(env("MEDIA_DIR", default="../media"))

# Database
DATABASES = {
	"default": env.db() if env("DATABASE_URL", default=None) else {}
}

# Cache
if env("CACHE_URL", default=None) :
	CACHES = {
		'default': env.cache()
	}

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

# E-mail
EMAIL_CONFIG = env.email_url("EMAIL_URL", default="filemail://../../filemail/")
vars().update(EMAIL_CONFIG)
DEFAULT_FROM_EMAIL = EMAIL_CONFIG["EMAIL_HOST_USER"]
SERVER_MAIL = EMAIL_CONFIG["EMAIL_HOST_USER"]

# Misc
SECRET_KEY = env("SECRET_KEY", default="NOT_NEEDED_FOR_DOCKER_BUILDS")
ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=[])

#############
#           #
#   DEBUG   #
#           #
#############

DEBUG = env("DEBUG")

# Debug Toolbar
if DEBUG:
	MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
	INSTALLED_APPS += [
		"debug_toolbar"
	]

INTERNAL_IPS = [
	"127.0.0.1",
] + env("DEBUG_IPS")

###############
#             #
#   PRIJAVA   #
#             #
###############

AUTH_USER_MODEL = 'dogodki_app.User'

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "dashboard"

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

##################
#                #
#   JEZIK, ČAS   #
#                #
##################

USE_I18N = True
USE_L10N = True

# Formati
DATE_FORMAT = "j. N Y"
DATETIME_FORMAT = "j. N Y H:m"

# Čas
TIME_ZONE = 'CET'
USE_TZ = True
