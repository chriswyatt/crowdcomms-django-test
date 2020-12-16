from django.utils import timezone
from rest_framework import viewsets

# Create your views here.
from rest_framework.permissions import IsAuthenticated

from analytics.models import UserVisit
from bunnies.models import Bunny, RabbitHole
from bunnies.permissions import RabbitHolePermissions
from bunnies.serializers import BunnySerializer, RabbitHoleSerializer


class RabbitHoleViewSet(viewsets.ModelViewSet):
    serializer_class = RabbitHoleSerializer
    permission_classes = (IsAuthenticated, RabbitHolePermissions)
    queryset = RabbitHole.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        kwargs = self.kwargs
        user = self.request.user

        # Regular users can only see their own RabbitHole objects
        if not user.is_superuser:
            queryset = queryset.filter(owner=user)

        if 'pk' in kwargs:
            hole_id = kwargs['pk']
            queryset = queryset.filter(id=hole_id)

        return queryset


class BunnyViewSet(viewsets.ModelViewSet):
    serializer_class = BunnySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Bunny.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            UserVisit.track_visit(user)

        return super().list(request, *args, **kwargs)
