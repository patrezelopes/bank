from django.contrib import admin

from .models import TransactionEntry, Transaction

admin.site.register(Transaction)
admin.site.register(TransactionEntry)
