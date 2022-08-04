import csv

from core.models import BankAccount, Transactions
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers


class BankAccountViewSet(viewsets.ModelViewSet):
    """View for manage bank account APIs."""

    serializer_class = serializers.BankAccountSerializer
    queryset = BankAccount.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve bank accounts for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-date")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'detail':
            return serializers.BankAccountDetailSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        self.perform_create(serializer)
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

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
        return self.queryset.filter(user=self.request.user).order_by("-transaction_date")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        # if self.action == 'detail':
        #     return serializers.BankAccountDetailSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        self.perform_create(serializer)
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """Create a new bank account."""
        serializer.save(user=self.request.user)
