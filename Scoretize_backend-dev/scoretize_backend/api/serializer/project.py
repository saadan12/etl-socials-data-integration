from ..serializers import serializers, Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        project = super(ProjectSerializer, self).create(validated_data)
        project.save()
        return project
