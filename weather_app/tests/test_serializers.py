from django.test import TestCase

from ..serializers import LongitudeLatitudeSerializer


class LongitudeLatitudeSerializerTest(TestCase):
    def test_valid_coordinates(self):
        data = {"latitude": 45.0, "longitude": 90.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["latitude"], 45.0)
        self.assertEqual(serializer.validated_data["longitude"], 90.0)

    def test_invalid_latitude_high(self):
        data = {"latitude": 91.0, "longitude": 50.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), "Invalid latitude"
        )

    def test_invalid_latitude_low(self):
        data = {"latitude": -91.0, "longitude": 50.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), "Invalid latitude"
        )

    def test_invalid_longitude_high(self):
        data = {"latitude": 45.0, "longitude": 181.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), "Invalid longitude"
        )

    def test_invalid_longitude_low(self):
        data = {"latitude": 45.0, "longitude": -181.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]), "Invalid longitude"
        )

    def test_missing_latitude(self):
        data = {"longitude": 50.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("latitude", serializer.errors)

    def test_missing_longitude(self):
        data = {"latitude": 50.0}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("longitude", serializer.errors)

    def test_non_numeric_coordinates(self):
        data = {"latitude": "abc", "longitude": "xyz"}
        serializer = LongitudeLatitudeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("latitude", serializer.errors)
        self.assertIn("longitude", serializer.errors)
