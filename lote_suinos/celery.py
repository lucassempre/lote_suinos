from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lote_suinos.settings')

app = Celery('lote_suinos')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

