from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Extendinf from this class to prevent errors about not implementing create and update methods"""

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
