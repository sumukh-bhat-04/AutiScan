import os
import django
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse, resolve
from django.template.loader import get_template

def run_checks():
    print("--- Starting Verification Checks ---")
    
    # Check URLs
    urls_to_check = [
        'password_reset',
        'password_reset_done',
        'password_reset_complete',
        # 'password_reset_confirm' needs args, so checking base resolution usually tricky without mock args
    ]
    
    print("\n[Check 1: URL Resolution]")
    for name in urls_to_check:
        try:
            url = reverse(name)
            print(f"[OK] URL '{name}' resolves to: {url}")
        except Exception as e:
            print(f"[FAIL] URL '{name}' validation failed: {e}")

    # Check Templates
    templates_to_check = [
        'registration/password_reset_form.html',
        'registration/password_reset_done.html',
        'registration/password_reset_confirm.html',
        'registration/password_reset_complete.html',
        'registration/password_reset_email.html',
    ]
    
    print("\n[Check 2: Template Existence]")
    for t_name in templates_to_check:
        try:
            t = get_template(t_name)
            print(f"[OK] Template found: {t_name}")
        except Exception as e:
            print(f"[FAIL] Template missing: {t_name} ({e})")

    # Check Email
    print("\n[Check 3: Email Sending]")
    try:
        # We shouldn't actually send a spam email to the user unless we want to, 
        # but the task requires verifying email sending.
        # I'll try to send one to the configured sender (self-test) or just print config.
        # Actually user said: "Email arrives to real Gmail inbox". 
        # I will send a test email to the configured EMAIL_HOST_USER.
        
        recipient = settings.EMAIL_HOST_USER
        print(f"Attempting to send test email to: {recipient}")
        
        send_mail(
            subject='Test Email from Django Verification Script',
            message='If you see this, email configuration is working correctly.',
            from_email=None, # Uses DEFAULT_FROM_EMAIL
            recipient_list=[recipient],
            fail_silently=False,
        )
        print("[OK] Email sent successfully (check inbox)")
    except Exception as e:
        print(f"[FAIL] Email sending failed: {e}")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    run_checks()
