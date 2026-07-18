import os
import django
from django.conf import settings
from django.template.loader import get_template

# Configure simple settings if not already configured
if not settings.configured:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'screening',
            'accounts',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
        ],
        STATIC_URL='/static/',
    )
    django.setup()

def verify_templates():
    templates_to_check = [
        'base.html',
        'home.html',
        'auth.html',
        'register.html',
        'dashboard.html',
        'profile.html',
        'predict.html',
        'result.html',
        'custom_admin.html',
        'history.html',
        'resources.html',
        'support.html',
    ]
    
    print("Verifying Templates...")
    for t in templates_to_check:
        try:
            get_template(t)
            print(f"[OK] {t} syntax is valid.")
        except Exception as e:
            print(f"[FAIL] {t} failed: {e}")

if __name__ == '__main__':
    verify_templates()
