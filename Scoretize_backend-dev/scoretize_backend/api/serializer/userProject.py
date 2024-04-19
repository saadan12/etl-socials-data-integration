from ..serializers import serializers, UserProject


class UserProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProject
        fields = '__all__'

    def create(self, validated_data):
        company = super(UserProjectSerializer, self).create(validated_data)
        company.save()
        return company
