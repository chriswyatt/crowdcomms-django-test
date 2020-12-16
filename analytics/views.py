from datetime import datetime

from analytics.models import UserVisit
from django.utils import timezone

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


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
                last_seen=now,
                user=user,
            )
            user_visit.visits += 1
            user_visit.save()

        data = {
            'version': 1.0,
            'time': now,
            'recent_visitors': 0,
            'all_visitors': 0,
            'all_visits': 0,
        }
        response = Response(data)

        return response

