from celery.schedules import crontab

schedules_function = {
    'refresh_user_statistics_materialized_view_every_week': {
        'task': 'refresh_user_statistics_materialized_view_every_week',
        'schedule': crontab(minute='*'),
    },
}
