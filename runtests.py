"""
Standalone test runner for iframeapi plugin
"""
import sys, os
from opal.core import application


class Application(application.OpalApplication):
    pass

from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    PROJECT_PATH=os.path.realpath(os.path.dirname(__file__)),
    TEMPLATE_DIRS=(
        os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            'iframeapi',
            'templates'
        ),
    ),
    OPAL_OPTIONS_MODULE='iframeapi.tests.dummy_options_module',
    ROOT_URLCONF='iframeapi.urls',
    STATIC_URL='/assets/',
    COMPRESS_ROOT='/tmp/',
    MIDDLEWARE_CLASSES=(
       'django.middleware.common.CommonMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'opal.middleware.AngularCSRFRename',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'opal.middleware.DjangoReversionWorkaround',
       'reversion.middleware.RevisionMiddleware',
       'axes.middleware.FailedLoginMiddleware',
    ),
    INSTALLED_APPS=('django.contrib.auth',
                   'django.contrib.contenttypes',
                   'django.contrib.sessions',
                   'django.contrib.staticfiles',
                   'django.contrib.admin',
                   'reversion',
                   'compressor',
                   'opal',
                   'iframeapi',
                   'iframeapi.tests',
                   )
)

import django
django.setup()

from django.test.runner import DiscoverRunner
test_runner = DiscoverRunner(verbosity=1)
if len(sys.argv) == 2:
    failures = test_runner.run_tests([sys.argv[-1], ])
else:
    failures = test_runner.run_tests(['iframeapi', ])
if failures:
    sys.exit(failures)
