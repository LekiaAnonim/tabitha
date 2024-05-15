from .base import *
import cloudinary

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"



# Configuration       
cloudinary.config( 
    cloud_name = "dlmcid90b", 
    api_key = "973926521247783", 
    api_secret = "iVA9j63HTBzTpwiR5k34cLujc8k", # Click 'View Credentials' below to copy your API secret
    secure=True
)



try:
    from .local import *
except ImportError:
    pass
