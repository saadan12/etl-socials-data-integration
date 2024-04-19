from ..serializers import serializers, Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        account = super(AccountSerializer, self).create(validated_data)
        account.save()
        return account
