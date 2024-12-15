from django.contrib import admin

from infrastructure.models.faucet_transaction import FaucetTransactionModel


@admin.register(FaucetTransactionModel)
class FaucetTransactionAdmin(admin.ModelAdmin):
    list_display = ("tx_hash", "wallet", "amount", "status", "created_at")
    search_fields = ("tx_hash", "wallet")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
