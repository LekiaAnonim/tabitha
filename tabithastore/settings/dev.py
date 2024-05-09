from .base import *
import cloudinary

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-*@v76v@zugliky3^8s4qht%+1zno*%#4r2foeh3sng2qft-a!a"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


cloudinary.config( 
  cloud_name = "dum5thngj", 
  api_key = "649654183492732", 
  api_secret = "DnhztD3mYzhHh33lb_rpJY8s7BE" 
)


try:
    from .local import *
except ImportError:
    pass
