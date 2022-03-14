import uuid

from rest_framework import serializers

from core.models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'account', 'value', 'currency', 'way']
        extra_kwarg = {
            'cod': {'read_only': True}
        }

    def create(self, validated_data):
        transaction_data = dict(status="pending", **validated_data)
        transaction = Transaction(**transaction_data)
        transaction.save()
        return transaction
