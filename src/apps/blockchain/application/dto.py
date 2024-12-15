from dataclasses import dataclass

from base.dto import BaseDTO, BaseEntityDTO


@dataclass(frozen=True)
class FaucetTransactionDTO(BaseEntityDTO):
    tx_hash: str

    @classmethod
    def from_entity(cls, entity) -> "FaucetTransactionDTO":
        return cls(tx_hash=entity.tx_hash.value)


@dataclass(frozen=True)
class FaucetStatsDTO(BaseDTO):
    total_pending: int
    total_successful: int
    total_failed: int

    @property
    def total_transactions(self) -> int:
        return self.total_pending + self.total_successful + self.total_failed
