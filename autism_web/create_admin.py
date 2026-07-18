import os
import django

def create_admin():
    from django.contrib.auth.models import User
    
    username = 'shadow'
    password = 'shadow'
    email = 'shadow@example.com'

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        User.objects.create_superuser(username, email, password)
        print("Superuser created successfully.")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    create_admin()
