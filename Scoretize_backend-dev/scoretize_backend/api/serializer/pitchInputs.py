from ..serializers import serializers, PitchInputs


class PitchInputsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PitchInputs
        fields = '__all__'

    def create(self, validated_data):
        project = super(PitchInputsSerializer, self).create(validated_data)
        project.save()
        return project
