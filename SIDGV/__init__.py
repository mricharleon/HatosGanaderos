from django.core import urlresolvers
from django.conf import settings

def reverse_decorator(func):
    def inner(*args, **kwargs):
        abs_path = func(*args,**kwargs)
        if settings.SSL_DOMAIN and settings.SSL_SECTIONS and settings.SSL_DOMAIN.startswith('https'):
            for section in settings.SSL_SECTIONS:
                if abs_path.startswith(section):
                    abs_path = settings.SSL_DOMAIN + abs_path
                    break
        return abs_path        
    return inner
urlresolvers.reverse = reverse_decorator(urlresolvers.reverse)