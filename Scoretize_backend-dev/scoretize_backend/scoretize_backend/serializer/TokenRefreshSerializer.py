from rest_framework import serializers


class TokenRefreshSerializer(serializers.Serializer):
    data = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )
