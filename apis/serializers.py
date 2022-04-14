from rest_framework import serializers
from .models import SingleImage


class SingleImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = SingleImage
    fields = ('id', 'name', 'image')