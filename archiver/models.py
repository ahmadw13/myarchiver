from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


def get_default_user():
    User = get_user_model()
    user, created = User.objects.get_or_create(username='default_user', defaults={
                                               'password': 'somehashedpassword'})
    return user.pk


class Archive(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=get_default_user
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    tags = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
