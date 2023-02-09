from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import post_created


@receiver(m2m_changed, sender=Post.category.through)
def post_create(instance, action, **kwargs):
    if action == 'post_add':
        post_created.delay(instance.id)