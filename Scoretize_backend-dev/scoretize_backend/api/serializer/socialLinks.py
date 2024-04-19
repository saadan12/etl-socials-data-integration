from ..serializers import serializers, Social_links


class SocialLinksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Social_links
        fields = '__all__'

    def create(self, validated_data):
        project = super(SocialLinksSerializer, self).create(validated_data)
        project.save()
        return project
