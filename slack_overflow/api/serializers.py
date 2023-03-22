from rest_framework import serializers
from core.models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["created", "text", "author", "project"]

