from rest_framework import serializers
from .models import EvictionRecord

class EvictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvictionRecord
        fields = '__all__'
