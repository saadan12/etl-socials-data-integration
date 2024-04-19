from ..serializers import serializers, Performance


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = '__all__'

    def create(self, validated_data):
        company = super(PerformanceSerializer, self).create(validated_data)
        company.save()
        return company
