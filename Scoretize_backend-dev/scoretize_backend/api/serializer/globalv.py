from ..serializers import serializers, Company_wise_scores


class GlobalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company_wise_scores
        fields = '__all__'
