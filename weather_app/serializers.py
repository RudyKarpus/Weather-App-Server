from OSMPythonTools.nominatim import Nominatim
from rest_framework import serializers

nominatim = Nominatim()


class LongitudeLatitudeSerializer(serializers.Serializer):

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        fields = ["latitude", "longitude"]

    def validate(self, attrs):
        latitude = attrs.get("latitude")
        longitude = attrs.get("longitude")
        if latitude > 90 or latitude < -90:
            raise serializers.ValidationError("Invalid latitude")

        if longitude > 180 or longitude < -180:
            raise serializers.ValidationError("Invalid longitude")

        return attrs
