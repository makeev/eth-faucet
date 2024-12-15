import logging
from datetime import timedelta

from apps.blockchain.application.dto import FaucetTransactionDTO
from apps.blockchain.application.exceptions import TooManyTransactionsFromIpError, TooManyTransactionsFromWalletError
from apps.blockchain.application.services.blockchain_service import BlockchainService
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
from apps.shared.value_objects.id import Id
from base.exceptions import BaseValidationError

logger = logging.getLogger(__name__)


class FaucetService:
    """FaucetService is responsible for managing faucet transactions and funding wallets with a specified amount of Ether.

    Attributes:
        blockchain_service (BlockchainService): Service to interact with the blockchain.
        faucet_transactions_repository (IFaucetTransactionsRepository): Repository to manage faucet transactions.
        threshold_timeout_minutes (int): Timeout threshold in minutes to prevent too many transactions from the same IP or wallet.
        amount_eth (str): Amount of Ether to fund the wallet.

    Methods:
        fund_wallet(ip_address: str, wallet_address: str) -> FaucetTransactionDTO:
            Args:
                ip_address (str): The IP address of the requester.
                wallet_address (str): The wallet address to fund.
            Returns:
                FaucetTransactionDTO: Data transfer object representing the faucet transaction.
            Raises:
                TooManyTransactionsFromIpError: If there are too many transactions from the same IP address.
                TooManyTransactionsFromWalletError: If there are too many transactions from the same wallet address.
                UndefinedError: If an undefined error occurs during the transaction process.
    """

    def __init__(
        self,
        blockchain_service: BlockchainService,
        faucet_transactions_repository: IFaucetTransactionsRepository,
        threshold_timeout_minutes: int,
        amount_eth: str,
    ):
        self.blockchain_service = blockchain_service
        self.faucet_transactions_repository = faucet_transactions_repository
        self.threshold_timeout_minutes = threshold_timeout_minutes
        self.amount_eth = amount_eth

    def fund_wallet(self, wallet_address: str, ip_address: str) -> FaucetTransactionDTO:
        """
        Creates a new faucet transaction and funds the wallet with the given amount.
        """
        # Check if there are too many transactions from the same IP address or wallet address
        ip = IPAddress(ip_address)
        last_ip_tx = self.faucet_transactions_repository.get_last_by_ip(ip.value)
        if last_ip_tx:
            minimum_next_tx_time = last_ip_tx.created_at + timedelta(minutes=self.threshold_timeout_minutes)
            if DomainDateTime.now() < minimum_next_tx_time:
                raise TooManyTransactionsFromIpError(ip)

        # Check if there are too many transactions from the same wallet address
        wallet = WalletAddress(wallet_address)
        last_wallet_tx = self.faucet_transactions_repository.get_last_by_wallet(wallet.value)
        if last_wallet_tx:
            minimum_next_tx_time = last_wallet_tx.created_at + timedelta(minutes=self.threshold_timeout_minutes)
            if DomainDateTime.now() < minimum_next_tx_time:
                raise TooManyTransactionsFromWalletError(wallet)

        tx_hash = None

        try:
            # Send funds to the wallet
            token_amount = TokenAmount.from_ether(self.amount_eth)
            tx_hash = self.blockchain_service.send_funds(wallet, token_amount)

            # Create a new faucet transaction
            faucet_transaction = FaucetTransaction(
                id=Id(),
                tx_hash=TransactionHash(tx_hash),
                ip_address=ip,
                wallet=wallet,
                amount=token_amount,
                status=TransactionStatus.PENDING,
            )
            tx = self.faucet_transactions_repository.create(faucet_transaction)
        except Exception as e:
            logger.exception("Error funding wallet")
            raise BaseValidationError(message="Error funding wallet: %s" % str(e)) from e
        else:
            return FaucetTransactionDTO.from_entity(tx)
