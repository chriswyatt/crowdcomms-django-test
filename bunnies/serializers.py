from django.db.models import Count
from rest_framework import serializers

from bunnies.models import Bunny, RabbitHole


class RabbitHoleSerializer(serializers.ModelSerializer):

    bunnies = serializers.PrimaryKeyRelatedField(many=True, queryset=Bunny.objects.all())
    bunny_count = serializers.SerializerMethodField()

    def validate_owner(self, owner):
        if self.instance is None:
            # When an object is initially created, ensure that the owner
            # is always the request user
            return self.context['request'].user
        else:
            return owner

    def get_bunny_count(self, obj):
        return obj.bunnies.count()

    class Meta:
        model = RabbitHole
        fields = ('location', 'bunnies', 'bunny_count', 'owner')


class BunnySerializer(serializers.ModelSerializer):

    home = serializers.SlugRelatedField(queryset=RabbitHole.objects.all(), slug_field='location')
    family_members = serializers.SerializerMethodField()

    def get_family_members(self, obj):
        queryset = obj.home.bunnies.exclude(pk=obj.pk)
        return queryset.values_list('name', flat=True)

    def validate(self, attrs):
        home = attrs['home']

        if home.bunnies.count() >= home.bunnies_limit:
            raise serializers.ValidationError("Bunny limit exceeded")

        return attrs

    class Meta:
        model = Bunny
        fields = ('name', 'home', 'family_members')

