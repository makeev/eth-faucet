from django.db import models

from apps.blockchain.domain.value_objects import TransactionStatus


class FaucetTransactionModel(models.Model):
    tx_hash = models.CharField(max_length=64, unique=True)  # Typical length for Ethereum tx hash
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices(),
    )
    ip_address = models.GenericIPAddressField(db_index=True)
    wallet = models.CharField(max_length=42, db_index=True)  # Standard Ethereum address length
    amount = models.IntegerField()  # For token amounts with high precision
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "faucet_transactions"

    def __str__(self):
        return f"Transaction {self.tx_hash} {self.amount} ETH to {self.wallet}"
