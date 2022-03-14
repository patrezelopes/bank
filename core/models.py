import uuid

from decouple import config
from djongo import models
from django.db import models as django_models

from bank.settings import DB_CLIENT


class Transaction(django_models.Model):
    STATUS_CHOICES = (('pending', 'Pending'), ('processing', 'Processing'), ('processed', 'Processed'),)
    WAY_CHOICES = (('out', 'Out'), ('in', 'In'),)

    cod = django_models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = django_models.CharField(max_length=60, verbose_name='User')
    account = django_models.CharField(max_length=60, verbose_name='Account')
    value = django_models.CharField(max_length=60, verbose_name='Value')
    currency = django_models.CharField(max_length=3, verbose_name='Currency')
    status = django_models.CharField(max_length=20, verbose_name='Status', choices=STATUS_CHOICES)
    way = django_models.CharField(max_length=10, verbose_name='Way', choices=WAY_CHOICES, default="pending")


class TransactionDjongo(models.Model):
    STATUS_CHOICES = (('pending', 'Pending'), ('processing', 'Processing'), ('processed', 'Processed'),)
    WAY_CHOICES = (('out', 'Out'), ('in', 'In'),)

    cod = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=60, verbose_name='User')
    account = models.CharField(max_length=60, verbose_name='Account')
    value = models.CharField(max_length=60, verbose_name='Value')
    currency = models.CharField(max_length=60, verbose_name='Currency')
    status = models.CharField(max_length=20, verbose_name='Status', choices=STATUS_CHOICES, default="pending")
    way = models.CharField(max_length=10, verbose_name='Way', choices=WAY_CHOICES)

    class Meta:
        abstract = True


class TransactionEntry(models.Model):
    transaction = models.EmbeddedField(
        model_container=Transaction,
    )
    objects = models.DjongoManager()

    class pymongo:

        db = DB_CLIENT[config('DB_NAME')]
        transactions = db['core_transactionentry']

        @staticmethod
        def create(**obj_data):
            return TransactionEntry.pymongo.transactions.insert_one(obj_data)

        @staticmethod
        def filter(**obj_data):
            return TransactionEntry.pymongo.transactions.find(obj_data)
