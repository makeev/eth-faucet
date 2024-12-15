from dataclasses import dataclass, field

from apps.blockchain.domain.value_objects import (
    IPAddress,
    TokenAmount,
    TransactionHash,
    TransactionStatus,
    WalletAddress,
)
from apps.shared.value_objects.datetime import DomainDateTime
from base.entity import BaseEntity


@dataclass
class FaucetTransaction(BaseEntity):
    tx_hash: TransactionHash | None
    status: TransactionStatus
    ip_address: IPAddress
    wallet: WalletAddress
    amount: TokenAmount
    created_at: DomainDateTime = field(default_factory=DomainDateTime.now)
    error: str | None = None
