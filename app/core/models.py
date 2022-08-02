"""
Database Models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.urls import reverse


class UserManager(BaseUserManager):
    """Manager for user models"""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("Email cannot be empty")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None):
        """Create a new superuser"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class BankAccount(models.Model):
    account_type = (
        ('savings', 'Savings'),
        ('credit', 'Credit'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bankaccount', on_delete=models.CASCADE, )
    account_type = models.CharField(max_length=20, choices=account_type, db_index=True )
    account_balance = models.FloatField(default=0)
    date = models.DateTimeField(auto_now=True, verbose_name='Transaction Date')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.account_type

    def get_absolute_url(self):
        return reverse('bank-detail', kwargs={'pk': self.pk})


class Transactions(models.Model):

    transaction_type = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE, )
    account_type = models.ForeignKey(BankAccount, related_name='accounttransactions', to_field='id', on_delete=models.CASCADE,)
    transaction_type = models.CharField(max_length=20, choices=transaction_type)
    transaction_amount = models.FloatField()
    transaction_date = models.DateTimeField(auto_now=True, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-transaction_date']


    def __str__(self):
        return self.transaction_type

    def get_absolute_url(self):
        return reverse('transaction-detail', kwargs={'pk': self.pk})
