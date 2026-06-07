from django.contrib.auth.models import User

username = "admin"
password = "Admin@12345"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")