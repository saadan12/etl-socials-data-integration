from ...serializers import serializers, Sector


class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = '__all__'


def create(self, validated_data):
    account = super(SectorSerializer, self).create(validated_data)
    account.save()
    return account
