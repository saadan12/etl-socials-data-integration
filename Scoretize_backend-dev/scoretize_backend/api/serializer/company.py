from ..serializers import serializers, Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

    def create(self, validated_data):
        company = super(CompanySerializer, self).create(validated_data)
        company.save()
        return company
