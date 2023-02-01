from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post


@receiver(m2m_changed, sender=Post.category.through)
def post_created(instance, action, **kwargs):
    if action == 'post_add':
        for i in instance.category.all():
            emails = User.objects.filter(subscriptions__category=i).values_list('email', flat=True)
            subject = 'Новая статья в категории:'
            for i in instance.category.all().values('category'):
                subject += f' {i.get("category")},'
            subject = subject[:-1] + '.'
            text_content = (
                f'{instance.title}\n'
                f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
            )
            html_content = (
                f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">{instance.title}</a>'
            )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()