from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.


class UserVisit(models.Model):
    '''
    We'll track each time a user visited the site
    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)
    visits = models.PositiveIntegerField(default=0)

    @classmethod
    def track_visit(cls, user, now=None):
        user_visit, _ = cls.objects.get_or_create(user=user)

        user_visit.last_seen = timezone.now() if now is None else now
        user_visit.visits += 1
        user_visit.save()
