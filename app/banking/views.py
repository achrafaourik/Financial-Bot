import csv

from core.models import BankAccount, Transactions
from . import serializers

from django.db.models import F

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# import django_filters.rest_framework


class BankAccountViewSet(viewsets.ModelViewSet):
    """View for manage bank account APIs."""

    serializer_class = serializers.BankAccountSerializer
    queryset = BankAccount.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        """Retrieve bank accounts for authenticated user."""
        account_type = self.request.query_params.get('account_type')

        if account_type:
            self.queryset = self.queryset.filter(account_type=account_type)

        return self.queryset.filter(user=self.request.user).order_by("-date")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'detail':
            return serializers.BankAccountDetailSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.BankAccountSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.BankAccountDetailSerializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Create a new bank account."""
        serializer.save(user=self.request.user)


class TransactionsViewSet(viewsets.ModelViewSet):
    """View for manage transactions APIs."""

    serializer_class = serializers.TransactionSerializer
    queryset = Transactions.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve bank accounts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by(
            "-transaction_date"
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bank_account = BankAccount.objects.get(user=self.request.user, id=request.data['account_type'])
        transaction_type = request.data['transaction_type']
        transaction_amount = float(request.data['transaction_amount'])

        if bank_account:
            print('found bank account')
            if transaction_type == 'deposit':
                bank_account.account_balance = F('account_balance') + transaction_amount
                bank_account.save()
            else:
                bank_account.account_balance = F('account_balance') - transaction_amount
                bank_account.save()
        else:
            print('did not find bank account')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """Create a new bank account."""
        serializer.save(user=self.request.user)
