from ..serializers import serializers, Users


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


def create(self, validated_data):
    company = super(Users, self).create(validated_data)
    company.save()
    return company
