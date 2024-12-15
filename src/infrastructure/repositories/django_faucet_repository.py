from apps.blockchain.domain.entities import FaucetTransaction
from apps.blockchain.domain.repository import IFaucetTransactionsRepository
from apps.blockchain.domain.value_objects import (
    IPAddress,
    TokenAmount,
    TransactionHash,
    TransactionStatus,
    WalletAddress,
)
from apps.shared.value_objects.datetime import DomainDateTime
from apps.shared.value_objects.id import RequiredId
from infrastructure.models.faucet_transaction import FaucetTransactionModel


class DjangoFaucetTransactionsRepository(IFaucetTransactionsRepository):
    def create(self, faucet_transaction: FaucetTransaction) -> FaucetTransaction:
        """Create a new faucet transaction or raise an exception if it already exists."""
        obj = FaucetTransactionModel.objects.create(
            tx_hash=faucet_transaction.tx_hash.value,
            status=faucet_transaction.status.value,
            ip_address=faucet_transaction.ip_address.value,
            wallet=faucet_transaction.wallet.value,
            amount=faucet_transaction.amount.to_wei(),
            error=faucet_transaction.error if faucet_transaction.error else None,
        )
        faucet_transaction.id = RequiredId(obj.pk)
        return faucet_transaction

    def update(self, faucet_transaction: FaucetTransaction) -> FaucetTransaction:
        """Update an existing faucet transaction."""
        obj = FaucetTransactionModel.objects.get(pk=faucet_transaction.pk.value)
        obj.tx_hash = faucet_transaction.tx_hash.value
        obj.status = faucet_transaction.status.value
        obj.ip_address = faucet_transaction.ip_address.value
        obj.wallet = faucet_transaction.wallet.value
        obj.amount = faucet_transaction.amount.to_wei()
        obj.error = faucet_transaction.error if faucet_transaction.error else None
        obj.save()
        return faucet_transaction

    def get_last_by_ip(self, ip_address: str) -> FaucetTransaction | None:
        """Get the last faucet transaction by IP address."""
        try:
            obj = FaucetTransactionModel.objects.filter(ip_address=ip_address).latest("created_at")
        except FaucetTransactionModel.DoesNotExist:
            return None
        return self.model_to_entity(obj)

    def get_last_by_wallet(self, wallet_address: str) -> FaucetTransaction | None:
        """Get the last faucet transaction by wallet address."""
        try:
            obj = FaucetTransactionModel.objects.filter(wallet=wallet_address).latest("created_at")
        except FaucetTransactionModel.DoesNotExist:
            return None
        return self.model_to_entity(obj)

    def get_pending_transactions(self) -> list[FaucetTransaction]:
        qs = FaucetTransactionModel.objects.filter(status=TransactionStatus.PENDING.value)
        return [self.model_to_entity(obj) for obj in qs]

    @classmethod
    def model_to_entity(cls, model: FaucetTransactionModel) -> FaucetTransaction:
        """Helper to convert a Django model instance to a domain entity."""
        return FaucetTransaction(
            id=RequiredId(model.pk),
            tx_hash=TransactionHash(model.tx_hash),
            status=TransactionStatus(model.status),
            ip_address=IPAddress(model.ip_address),
            wallet=WalletAddress(model.wallet),
            amount=TokenAmount(model.amount),
            created_at=DomainDateTime(model.created_at),
            error=model.error if model.error else None,
        )
