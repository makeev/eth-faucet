from dataclasses import dataclass

from base.dto import BaseDTO


@dataclass(frozen=True)
class FaucetTransactionDTO(BaseDTO):
    tx_hash: str

    @classmethod
    def from_entity(cls, entity):
        return cls(tx_hash=entity.tx_hash.value)
