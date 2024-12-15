from abc import ABC, abstractmethod

from apps.blockchain.domain.entities import FaucetTransaction


class IFaucetTransactionsRepository(ABC):
    """
    Interface for FaucetTransaction repository.

    This interface defines the methods required for creating and retrieving
    faucet transactions based on IP address and wallet address.
    """

    @abstractmethod
    def create(self, faucet_transaction: FaucetTransaction) -> FaucetTransaction: ...

    @abstractmethod
    def get_last_by_ip(self, ip_address: str) -> FaucetTransaction | None: ...

    @abstractmethod
    def get_last_by_wallet(self, wallet_address: str) -> FaucetTransaction | None: ...
