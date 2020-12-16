from datetime import timedelta

from analytics.models import UserVisit
from django.db.models import Count, Sum
from django.db.models.query_utils import Q
from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


OLD_USER_THRESHOLD = timedelta(hours=3)


class HelloWorld(APIView):
    """
    Basic 'Hello World' view. Show our current API version, the current time, the number of recent visitors
    in the last 1 hour, and the total number of visitors and page visits
    """

    def get(self, request, format=None):
        now = timezone.now()
        user = request.user

        if user.is_authenticated:
            (user_visit,
             user_visit_created) = UserVisit.objects.get_or_create(
                user=user,
            )
            user_visit.last_seen = now
            user_visit.visits += 1
            user_visit.save()

        recent_user_filter = Q(last_seen__gt=now - OLD_USER_THRESHOLD)

        data = {
            'version': 1.0,
            'time': now,
            **UserVisit.objects.aggregate(
                all_visitors=Count('user'),
                recent_visitors=Count(
                    'user',
                    filter=recent_user_filter,
                ),
                all_visits=Sum('visits'),
            )}

        response = Response(data)

        return response
