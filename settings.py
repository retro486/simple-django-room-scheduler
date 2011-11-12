#################################
# Custom settings for rooms app

# The number of hours to look ahead on the front page; make sure this is some
# factor of 0.5 or else the table footer won't render correctly.
RES_LOOK_AHEAD_HOURS = 6.5

# The default template to use for the front page
RES_DEFAULT_TEMPLATE = 'rooms/only_now.html'

# The temporary URL to the modified VuFind driver.pl file on the biblio server:
#RES_BARCODE_URL = 'http://biblio.ern.nps.edu/vufind/?query=checkBarcode&patronId='
RES_BARCODE_URL = 'http://localhost/barcode.html?'
#NOTE: this will eventually be replaced with SIP2 auth.

# Prevent users from requesting reservations that occur in the past?
RES_ENFORCE_NO_PAST = True

# A list of tuples containing value, key pairs for reservations. Mostly for
# statistics and for blocking off rooms to prevent bookings on holidays or
# other days when the rooms are unavailable (under construction for example)
# NOTE: any value of -1 will be blocked off on the calender and shown in the
# legend and on the calendar with the "closed" styles and a value of 1 will
# represent a normal reservation. No other values are used internally.
RES_TYPE_CHOICES = (
	(1, 'Normal'),
	(-1, 'Closed'),
)

# User quotas: enable them and if so, how many hours PER DAY to users get?
RES_ENFORCE_DAILY_QUOTA = False
RES_DAILY_QUOTA = 4.00 # decimal value in hours, regardless of room selection
#NOTE: not sure how this would affect the DB if you change the format, i.e., xx.x or x.xxx or xxx.x etc.

# Allow refunds of quota time if users turn in their keys early.
RES_ALLOW_REFUNDS = True

# More user quotas: enable maximum # of reservations (independent of max # of hours per day) and how
# many reservations per day (TOTAL, regardless of room selection) do users get?
RES_ENFORCE_MAX_NUM = True
RES_MAX_NUM = 3 # users get up to 3 reservations per day, regardless of room selection

# Enfore allowing users to only be able to have a single reservation for any room
# at any given time.
RES_ENFORCE_OAAT = True

# Enforce a minimum time on meetings and if so what amount of time is minimal
# Helps prevent blocking off many small amounts of time. Can be used independent
# of ENFORCE_MAX_RES.
RES_ENFORCE_MIN_LENGTH = True
RES_MIN_LENGTH = 30 # minutes

# Ignore the following user accounts when dealing with quotas:
RES_ADMINS = ('libsys@nps.edu',)

# END custom settings for rooms app
#######################################

# Django settings for studyrooms project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/html/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://172.20.113.114:8008/media'
MEDIA_URL = 'http://localhost/media/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/russ/repos/studyrooms/templates',
	#'/usr/local/dklstudy/studyrooms/templates',
)

ADMINS = (
    ('Russell Bernhardt', 'rgbernha@nps.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l==+ynwudpf$b%%!lmuyfw!#!roqcw9llute2sq&u@@a4*oa(y'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'studyrooms.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin', # for manual mgmt of data
	'south',
    'rooms',
	'roomkeys',
)
