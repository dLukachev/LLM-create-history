from celery import Celery

app_celery = Celery('llm_create_history', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
