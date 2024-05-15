from .base import *
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
DEBUG = env('DEBUG')

ALLOWED_HOST = ['*']

# djangostripe/settings.py

STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE' : [
            'profile',
            'email'
        ],
        'APP': {
            'client_id': env('CLIENT_ID'),
            'secret': env('CLIENT_SECRET'),
            'key': ''
        },
        'AUTH_PARAMS': {
            'access_type':'online',
        }
    }
}

try:
    from .local import *
except ImportError:
    pass
