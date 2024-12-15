import ipaddress
from dataclasses import dataclass
from enum import Enum

from eth_typing.encoding import HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3.types import Wei


class TransactionStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    # currently all our statuses will be pending, but we may want to change this in the future
    PENDING = "pending"

    @classmethod
    def choices(cls):
        return [(tag.value, tag.name) for tag in cls]


@dataclass(frozen=True)
class WalletAddress:
    value: str

    def __post_init__(self):
        if not Web3.is_address(self.value):
            raise ValueError(f"Invalid Ethereum address: {self.value}")

        checksummed = Web3.to_checksum_address(self.value)
        object.__setattr__(self, "value", checksummed)


@dataclass(frozen=True)
class TransactionHash:
    value: str

    def __post_init__(self):
        object.__setattr__(self, "value", Web3.to_hex(hexstr=self.value.lower()))  # type: ignore

    @property
    def bytes(self) -> HexBytes:
        return HexBytes(Web3.to_bytes(hexstr=HexStr(self.value)))


@dataclass(frozen=True)
class IPAddress:
    value: str

    def __post_init__(self):
        try:
            ipaddress.ip_address(self.value)
        except ValueError:
            raise ValueError(f"Invalid IP address: {self.value}")

    def to_int(self):
        return int(ipaddress.ip_address(self.value))

    @property
    def version(self):
        return ipaddress.ip_address(self.value).version


@dataclass(frozen=True)
class TokenAmount:
    wei_value: int

    def __post_init__(self):
        if self.wei_value <= 0:
            raise ValueError("Token amount must be positive in wei.")

    @classmethod
    def from_ether(cls, ether_amount: str) -> "TokenAmount":
        wei_value = Web3.to_wei(str(ether_amount), "ether")
        if wei_value <= 0:
            raise ValueError("Token amount must be positive.")
        return cls(wei_value=wei_value)

    @classmethod
    def from_int(cls, int_amount: int) -> "TokenAmount":
        if int_amount <= 0:
            raise ValueError("Token amount must be positive.")
        return cls(wei_value=int_amount)

    def to_wei(self) -> Wei:
        return Web3.to_wei(self.wei_value, "wei")
