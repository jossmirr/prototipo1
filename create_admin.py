# create_admin.py (coloca esto en la raíz de tu proyecto)
import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_app.settings')  # Ajusta a tu proyecto
django.setup()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superusuario creado.")
else:
    print("El superusuario ya existe.")
