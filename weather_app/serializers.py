from OSMPythonTools.nominatim import Nominatim
from rest_framework import serializers

nominatim = Nominatim()


class LongitudeLatitudeSerializer(serializers.Serializer):
    """Serializer for validating latitude and longitude

    Args:
        latitude: geographical latitude
        longitude: geographical longitude

    Returns:
        Validaded data of latitude and longitude
    """

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        fields = ["latitude", "longitude"]

    def validate(self, attrs):
        """
        Validates based on proper latitude and longitude range.
        """
        latitude = attrs.get("latitude")
        longitude = attrs.get("longitude")
        if latitude > 90 or latitude < -90:
            raise serializers.ValidationError("Invalid latitude")

        if longitude > 180 or longitude < -180:
            raise serializers.ValidationError("Invalid longitude")

        return attrs
