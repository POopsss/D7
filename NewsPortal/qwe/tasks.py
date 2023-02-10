from datetime import datetime, timezone, timedelta
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscription


@shared_task
def weekly_news():
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
                    text = '\n'.join(
                        ''f'{post.title} -- http://127.0.0.1:8000{post.get_absolute_url()};  ' for post in post_list)
                    text_html = '\n'.join(
                        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">{post.title}</a>;  ' for post in
                        post_list)
                else:
                    subject = 'Новые статьи за последнюю неделю'
                    text = 'Новых статей по вашим подпискам за последнюю неделю не публиковалось =('
                    text_html = 'Новых статей по вашим подпискам за последнюю неделю не публиковалось =('
                msg = EmailMultiAlternatives(subject, text, None, [user.email])
                msg.attach_alternative(text_html, "text/html")
                msg.send()


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