import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogengine.settings")

app = Celery('blogengine')
app.config_from_object('django.conf:settings')


app.autodiscover_tasks(['blog', 'weather'])
