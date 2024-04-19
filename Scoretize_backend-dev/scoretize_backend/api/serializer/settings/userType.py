from ...serializers import serializers, User_Type


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Type
        fields = '__all__'


def create(self, validated_data):
    account = super(UserTypeSerializer, self).create(validated_data)
    account.save()
    return account
