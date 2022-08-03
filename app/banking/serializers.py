from rest_framework import serializers
from core.models import BankAccount, Transactions, User


class TransactionSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False,)
    account_type = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(), many=False,
    )

    class Meta:
        model = Transactions
        fields = [
            "id",
            "transaction_date",
            "account_type",
            "user",
            "transaction_type",
            "transaction_amount",
        ]


class BankAccountSerializer(serializers.ModelSerializer):
    """Serializer for Bank account."""

    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),many=False,)
    # account_transactions = TransactionSerializer(many=True, read_only=True, )

    class Meta:
        model = BankAccount
        fields = ["id", "date", "account_type", "account_balance"]
        extra_kwargs = {
            "account_balance": {
                # 'read_only': True,
                "required": True
            },
            "account_type": {"required": True},
        }
        read_only_fields = ["id"]


# class BankAccountDetailSerializer(BankAccountSerializer):
#     """Serializer for bank account detail view."""

#     class Meta(BankAccountSerializer.Meta):
#         fields = BankAccountSerializer.Meta.fields + ['account_transactions']
