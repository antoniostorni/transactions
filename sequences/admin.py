from django.contrib import admin

# Register your models here.
from .models import Sequence, Transaction


class SequenceAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'amount', 'description', 'sequence']


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Sequence, SequenceAdmin)
