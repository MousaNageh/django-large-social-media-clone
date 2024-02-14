from celery.schedules import crontab


schedules_function = {
    "refresh_user_statistics_materialized_view_every_week": {
        "task": "refresh_user_statistics_materialized_view_every_week",
        "schedule": crontab(
            hour="2", minute="0", day_of_week="5"
        ),  # every Friday at exactly 2 AM.
    },
}
