from celery import Celery
from celery.schedules import crontab

from worker_celery.config import get_config

config = get_config()

app = Celery(broker=f"{config.CELERY_BROKER_URL}", backend=None)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-health-check': {
        'task': 'check',
        'schedule': crontab(minute='*/1'),
    },
}
app.conf.timezone = 'UTC'


from core.tasks import get_cash_out, get_cash_in
get_cash_out.delay()
get_cash_in.delay()
