from src.monitors import monitor_names, monitors
from src.utils.prometheus_metric import PrometheusMetric, PrometheusType

MONITORS = monitors.MONITORS


# Returns active celery tasks
def get_celery_tasks():
    celery_tasks = monitors.get_monitors(
        [
            MONITORS[monitor_names.celery_tasks],
        ]
    )

    return celery_tasks


def celery_tasks_prometheus_exporter():

    tasks = get_celery_tasks()["celery_tasks"]

    metric = PrometheusMetric(
        "celery_running_tasks",
        "The currently running celery tasks",
        labelnames=["task_name"],
        metric_type=PrometheusType.GAUGE,
    )

    for task in tasks:
        metric.save_time({"task_name": task["name"]}, start_time=task["time_start"])


PrometheusMetric.register_collector(
    "celery_tasks_prometheus_exporter", celery_tasks_prometheus_exporter
)