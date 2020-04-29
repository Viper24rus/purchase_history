from rest_framework import serializers

from .models import Customer, Gem


class CustomerSerializer(serializers.ModelSerializer):
    gems = serializers.StringRelatedField(many=True,)

    class Meta:
        model = Customer
        fields = ['username', 'spent_money', 'gems']
