# Import all configs from serializers.py
from ..serializers import serializers, Validations, Users


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.CharField(
        validators=[Validations.email]
    )

    name = serializers.CharField(
        validators=[Validations.name]
    )

    surname = serializers.CharField(
        validators=[Validations.name]
    )

    password = serializers.CharField(
        validators=[Validations.password]
    )

    class Meta:
        model = Users
        fields = '__all__'

    # hashing password

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
