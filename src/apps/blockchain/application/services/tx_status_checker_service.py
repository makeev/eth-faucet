import logging
from time import sleep

from apps.blockchain.application.services.blockchain_service import BlockchainService
from apps.blockchain.domain.repository import IFaucetTransactionsRepository
from apps.blockchain.domain.value_objects import TransactionStatus

logger = logging.getLogger(__name__)


class TxStatusCheckerService:
    def __init__(
        self,
        blockchain_service: BlockchainService,
        faucet_transactions_repository: IFaucetTransactionsRepository,
        loop_timeout_seconds: int,
    ):
        self.blockchain_service = blockchain_service
        self.faucet_transactions_repository = faucet_transactions_repository
        self.loop_timeout_seconds = loop_timeout_seconds
        self._is_running = True

    def run(self):
        while self._is_running:
            logger.debug("Checking pending transactions...")
            try:
                transactions_to_check = self.faucet_transactions_repository.get_pending_transactions()
                for transaction in transactions_to_check:
                    tx_hash = transaction.tx_hash
                    tx_status = self.blockchain_service.get_transaction_status(tx_hash)
                    if tx_status != TransactionStatus.PENDING:
                        transaction.status = tx_status
                        self.faucet_transactions_repository.update(transaction)
            finally:
                sleep(self.loop_timeout_seconds)

        logger.debug("TxStatusCheckerService stopped")

    def stop(self):
        self._is_running = False
