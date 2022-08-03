import csv

from core.models import BankAccount
from core.models import User as CustomUser
from django.http import Http404
from django.http.response import HttpResponse
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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
