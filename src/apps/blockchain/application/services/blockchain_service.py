import logging

from eth_account.signers.local import LocalAccount
from eth_account.types import TransactionDictType
from web3 import Web3

from apps.blockchain.domain.value_objects import TokenAmount, TransactionHash, TransactionStatus, WalletAddress

logger = logging.getLogger(__name__)


class BlockchainService:
    def __init__(self, provider_url: str, chain_id: int, account: LocalAccount):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = account
        self.chain_id = chain_id

    def send_funds(self, to_address: WalletAddress, amount: TokenAmount) -> str:
        nonce = self.web3.eth.get_transaction_count(self.account.address)

        tx: TransactionDictType = {
            "nonce": nonce,
            "to": to_address.checksum_address,
            "value": amount.to_wei(),
            "gasPrice": self.web3.eth.gas_price,
            "chainId": self.chain_id,
            "from": self.account.address,
        }

        gas_estimate = self.web3.eth.estimate_gas(tx)  # type: ignore
        tx["gas"] = gas_estimate

        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex()

    def get_transaction_status(self, tx_hash: TransactionHash) -> TransactionStatus:
        """
        Check transaction status by hash.
        """
        try:
            # Get transaction
            tx_receipt = self.web3.eth.get_transaction_receipt(tx_hash.bytes)

            if tx_receipt is None:
                return TransactionStatus.PENDING

            # Check transaction status
            # status 1 = success, status 0 = failure
            if tx_receipt.get("status") == 1:
                return TransactionStatus.SUCCESS
            return TransactionStatus.FAILED
        except Exception as e:
            logger.error(f"Error checking transaction status for {tx_hash.value}: {str(e)}")
            # TODO: maybe better not to return PENDING here? OR some other status like UNKNOWN?
            return TransactionStatus.PENDING
