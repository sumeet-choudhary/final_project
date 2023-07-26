from celery import Celery


def make_celery(application):
    celery_app = Celery(application, broker="amqp://rabbitmq:5672/", include=['application.celery_config.celery_task'])
    return celery_app
