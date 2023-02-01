import logging

from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from qwe.models import Post, Subscription

logger = logging.getLogger(__name__)


def my_job(instance=None):
    for user in User.objects.all():
        if user.email:
            if Subscription.objects.filter(user=user):
                post_list = []
                for subscription in Subscription.objects.filter(user=user):
                    for post in Post.objects.filter(
                            category=subscription.category,
                            date__gt=datetime.now(timezone.utc) - timedelta(days=7)
                    ):
                        if post not in post_list:
                            post_list.append(post)
                if post_list:
                    subject = 'Новые статьи за последнюю неделю'
                    text = '\n'.join(''f'{post.title} -- http://127.0.0.1:8000{post.get_absolute_url()};  ' for post in post_list)
                    text_html = '\n'.join(f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a>;  ' for post in post_list)
                else:
                    subject = 'Новые статьи за последнюю неделю'
                    text = 'Новых статей по вашим подпискам за последнюю неделю не публиковалось =('
                    text_html = 'Новых статей по вашим подпискам за последнюю неделю не публиковалось =('
                msg = EmailMultiAlternatives(subject, text, None, [user.email])
                msg.attach_alternative(text_html, "text/html")
                msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute="0", hour="18", day_of_week='4'),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

