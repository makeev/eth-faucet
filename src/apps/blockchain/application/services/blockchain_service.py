import logging

from eth_account import Account
from web3 import Web3
from web3.types import TxParams

from apps.blockchain.domain.value_objects import TokenAmount, WalletAddress

logger = logging.getLogger(__name__)


class BlockchainService:
    def __init__(self, provider_url: str, mnemonic: str, chain_id: int):
        Account.enable_unaudited_hdwallet_features()
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.web3.eth.account.from_mnemonic(mnemonic)
        logging.debug("using faucet account %s" % self.account.address)
        self.chain_id = chain_id

    def send_funds(self, to_address: WalletAddress, amount: TokenAmount) -> str:
        nonce = self.web3.eth.get_transaction_count(self.account.address)

        tx: TxParams = {
            "nonce": nonce,
            "to": to_address.value,
            "value": amount.to_wei(),
            "gasPrice": self.web3.eth.gas_price,
            "chainId": self.chain_id,
            "from": self.account.address,
        }

        gas_estimate = self.web3.eth.estimate_gas(tx)
        tx["gas"] = gas_estimate

        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex()
