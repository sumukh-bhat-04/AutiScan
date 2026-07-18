import os
import django
from django.conf import settings
from django.template.loader import get_template

def debug_templates():
    print(f"BASE_DIR: {settings.BASE_DIR}")
    print(f"TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")
    print(f"Attempting to find 'registration/password_reset_form.html'...")
    
    try:
        t = get_template('registration/password_reset_form.html')
        print(f"SUCCESS: Found at {t.origin.name}")
    except Exception as e:
        print(f"FAILURE: {e}")
        
    print("\nChecking file existence manually:")
    expected_path = os.path.join(settings.BASE_DIR, 'templates', 'registration', 'password_reset_form.html')
    print(f"Looking for: {expected_path}")
    if os.path.exists(expected_path):
        print("File EXISTS on disk at expected path.")
    else:
        print("File does NOT exist at expected path.")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    debug_templates()
