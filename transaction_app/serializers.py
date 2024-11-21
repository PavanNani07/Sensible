from rest_framework import serializers
from .models import Transaction
from django.contrib.auth.models import User

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'amount', 'transaction_type', 'status', 'user', 'timestamp']
        read_only_fields = ['transaction_id', 'timestamp', 'status']


class TransactionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True, 'choices': ['COMPLETED', 'FAILED']}
        }
