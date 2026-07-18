import os
import django
from django.urls import reverse
from django.test import RequestFactory

def verify_admin():
    from django.contrib.auth.models import User
    
    print("--- Verifying Admin Setup ---")
    
    # 1. Verify User
    try:
        user = User.objects.get(username='shadow')
        print(f"[OK] Superuser 'shadow' found. Is superuser: {user.is_superuser}")
        if not user.check_password('shadow'):
            print("[WARN] Password for 'shadow' might not be 'shadow'. Setting it now...")
            user.set_password('shadow')
            user.save()
            print("[OK] Password set to 'shadow'.")
        else:
            print("[OK] Password check passed.")
    except User.DoesNotExist:
        print("[FAIL] Superuser 'shadow' NOT found.")

    # 2. Verify URL
    try:
        url = reverse('admin:index')
        print(f"[OK] Admin URL resolves to: {url}")
    except Exception as e:
        print(f"[FAIL] Admin URL resolution failed: {e}")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    verify_admin()
