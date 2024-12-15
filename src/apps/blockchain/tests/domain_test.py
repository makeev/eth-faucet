import pytest
from hexbytes import HexBytes
from web3 import Web3

from apps.blockchain.domain.entities import FaucetTransaction
from apps.blockchain.domain.value_objects import (
    IPAddress,
    TokenAmount,
    TransactionHash,
    TransactionStatus,
    WalletAddress,
)
from apps.shared.value_objects.datetime import DomainDateTime
from apps.shared.value_objects.id import Id

# Test data
VALID_WALLET = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
INVALID_WALLET = "0xinvalid"
VALID_TX_HASH = "0x9fc76417374aa880d4449a1f7f31ec597f00b1f6f3dd2d66f4c9c6c445836d8b"
INVALID_TX_HASH = "invalid"
VALID_IP = "192.168.1.1"
INVALID_IP = "256.256.256.256"


class TestWalletAddress:
    def test_valid_wallet_address(self):
        wallet = WalletAddress(VALID_WALLET)
        assert wallet.value == Web3.to_checksum_address(VALID_WALLET)

    def test_invalid_wallet_address(self):
        with pytest.raises(ValueError, match="Invalid Ethereum address"):
            WalletAddress(INVALID_WALLET)

    def test_lowercase_wallet_address_converts_to_checksum(self):
        lowercase_address = VALID_WALLET.lower()
        wallet = WalletAddress(lowercase_address)
        assert wallet.value == Web3.to_checksum_address(lowercase_address)


class TestTransactionHash:
    def test_valid_transaction_hash(self):
        tx_hash = TransactionHash(VALID_TX_HASH)
        assert tx_hash.value == VALID_TX_HASH.lower()

    def test_transaction_hash_without_0x(self):
        hash_without_0x = VALID_TX_HASH[2:]
        tx_hash = TransactionHash(hash_without_0x)
        assert tx_hash.value.startswith("0x")

    def test_transaction_hash_bytes_property(self):
        tx_hash = TransactionHash(VALID_TX_HASH)
        assert isinstance(tx_hash.bytes, HexBytes)


class TestIPAddress:
    def test_valid_ipv4_address(self):
        ip = IPAddress(VALID_IP)
        assert ip.value == VALID_IP
        assert ip.version == 4

    def test_valid_ipv6_address(self):
        ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        ip = IPAddress(ipv6)
        assert ip.value == ipv6
        assert ip.version == 6

    def test_invalid_ip_address(self):
        with pytest.raises(ValueError, match="Invalid IP address"):
            IPAddress(INVALID_IP)

    def test_ip_to_int_conversion(self):
        ip = IPAddress(VALID_IP)
        assert isinstance(ip.to_int(), int)


class TestTokenAmount:
    def test_valid_token_amount_from_wei(self):
        amount = TokenAmount(1000)
        assert amount.wei_value == 1000

    def test_invalid_zero_token_amount(self):
        with pytest.raises(ValueError, match="Token amount must be positive"):
            TokenAmount(0)

    def test_invalid_negative_token_amount(self):
        with pytest.raises(ValueError, match="Token amount must be positive"):
            TokenAmount(-1)

    def test_from_ether_conversion(self):
        amount = TokenAmount.from_ether("1.0")
        assert amount.wei_value == Web3.to_wei(1, "ether")

    def test_from_int_conversion(self):
        amount = TokenAmount.from_int(1000)
        assert amount.wei_value == 1000

    def test_to_wei_conversion(self):
        amount = TokenAmount(1000)
        assert amount.to_wei() == 1000


class TestTransactionStatus:
    def test_transaction_status_values(self):
        assert TransactionStatus.SUCCESS.value == "success"
        assert TransactionStatus.FAILED.value == "failed"
        assert TransactionStatus.PENDING.value == "pending"

    def test_transaction_status_choices(self):
        choices = TransactionStatus.choices()
        assert len(choices) == 3
        assert ("success", "SUCCESS") in choices
        assert ("failed", "FAILED") in choices
        assert ("pending", "PENDING") in choices


class TestFaucetTransaction:
    def test_create_valid_faucet_transaction(self):
        tx = FaucetTransaction(
            id=Id(),
            tx_hash=TransactionHash(VALID_TX_HASH),
            status=TransactionStatus.PENDING,
            ip_address=IPAddress(VALID_IP),
            wallet=WalletAddress(VALID_WALLET),
            amount=TokenAmount(1000),
            error=None,
        )

        assert isinstance(tx.created_at, DomainDateTime)
        assert tx.tx_hash.value == VALID_TX_HASH.lower()
        assert tx.status == TransactionStatus.PENDING
        assert tx.ip_address.value == VALID_IP
        assert tx.wallet.value == Web3.to_checksum_address(VALID_WALLET)
        assert tx.amount.wei_value == 1000
        assert tx.error is None

    def test_faucet_transaction_with_error(self):
        error_message = "Transaction failed"
        tx = FaucetTransaction(
            id=Id(),
            tx_hash=TransactionHash(VALID_TX_HASH),
            status=TransactionStatus.FAILED,
            ip_address=IPAddress(VALID_IP),
            wallet=WalletAddress(VALID_WALLET),
            amount=TokenAmount(1000),
            error=error_message,
        )

        assert tx.status == TransactionStatus.FAILED
        assert tx.error == error_message
