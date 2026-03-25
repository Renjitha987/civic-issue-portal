import os
import django
import traceback

os.environ['DJANGO_SETTINGS_MODULE'] = 'civic_portal.settings'
try:
    django.setup()
except Exception:
    traceback.print_exc()
