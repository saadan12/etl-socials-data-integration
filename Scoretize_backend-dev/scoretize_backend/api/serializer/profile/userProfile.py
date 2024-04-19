# Import all configs from serializers.py
from ...serializers import serializers, Users, Validations


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(
        validators=[Validations.email]
    )

    name = serializers.CharField(
        validators=[Validations.name]
    )

    surname = serializers.CharField(
        validators=[Validations.name]
    )

    class Meta:
        model = Users
        fields = ('email', 'name', 'surname', 'is_emailMarketing')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(validators=[Validations.password])
    new_password = serializers.CharField(validators=[Validations.password])
    new_password_confirm = serializers.CharField(
        validators=[Validations.password])

    def validate_old_password(self, value):
        if not self.context['user'].check_password(value):
            raise serializers.ValidationError('Incorrect current password')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                'Your password and confirmation password do not match.')
        return data
