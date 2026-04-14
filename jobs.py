import rq
from rq import registry


def get_jobs_state():
    started_registry = registry.StartedJobRegistry(queue=queue)
    canceled_registry = registry.CanceledJobRegistry(queue=queue)
    failed_registry = registry.FailedJobRegistry(queue=queue)
    scheduled_registry = registry.ScheduledJobRegistry(queue=queue)

    started = started_registry.get_job_ids()
    candeled = canceled_registry.get_job_ids()
    failed = failed_registry.get_job_ids()
    scheduled = scheduled_registry.get_job_ids()
