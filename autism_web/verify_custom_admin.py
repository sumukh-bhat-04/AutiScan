import os
import django
from django.urls import reverse
from django.test import Client

def verify_dashboard():
    from django.contrib.auth.models import User
    
    print("--- Verifying Custom Admin Dashboard ---")
    
    client = Client()
    
    # 1. Check URL Resolution
    try:
        url = reverse('admin_dashboard')
        print(f"[OK] URL resolved: {url}")
    except Exception as e:
        print(f"[FAIL] URL resolution failed: {e}")
        return

    # 2. Check Access (Unauthenticated)
    resp = client.get(url)
    if resp.status_code == 302:
        print("[OK] Unauthenticated access redirects (Correct).")
    else:
        print(f"[FAIL] Unauthenticated access got status {resp.status_code}")

    # 3. Check Access (Superuser)
    try:
        user = User.objects.get(username='shadow')
        client.force_login(user)
        resp = client.get(url)
        if resp.status_code == 200:
            print("[OK] Superuser 'shadow' can access dashboard.")
            if b'Administrator Dashboard' in resp.content:
                print("[OK] Dashboard template verified (Title found).")
            else:
                 print("[WARN] Dashboard loaded but title not found.")
                 
            # Check for Modal presence
            if b'id="userModal"' in resp.content:
                print("[OK] User List Modal found.")
            else:
                print("[FAIL] User List Modal missing.")
                
            # Check for "Dashboard" link hiding style
            if b'.header div a[href="/dashboard/"]' in resp.content:
                print("[OK] Dashboard link hiding style found.")
            else:
                print("[WARN] Dashboard link hiding style missing or changed.")
        else:
            print(f"[FAIL] Superuser access failed with status {resp.status_code}")
    except User.DoesNotExist:
        print("[FAIL] User 'shadow' does not exist so cannot verify login access.")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    verify_dashboard()
