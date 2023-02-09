from celery import shared_task
from .management.commands.runapscheduler import my_job
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Post


@shared_task
def weekly_news():
    my_job()
    print('Рассылка прошла')


@shared_task
def post_created(instance_id):
    for i in Post.objects.get(id=instance_id).category.all():
        emails = User.objects.filter(subscriptions__category=i).values_list('email', flat=True)
        subject = 'Новая статья в категории:'
        for i in Post.objects.get(id=instance_id).category.all().values('category'):
            subject += f' {i.get("category")},'
        subject = subject[:-1] + '.'
        text_content = (
            f'{Post.objects.get(id=instance_id).title}\n'
            f'Ссылка на статью: http://127.0.0.1:8000{Post.objects.get(id=instance_id).get_absolute_url()}'
        )
        html_content = (
            f'<a href="http://127.0.0.1:8000{Post.objects.get(id=instance_id).get_absolute_url()}">{Post.objects.get(id=instance_id).title}</a>'
        )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()