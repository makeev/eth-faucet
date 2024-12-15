from dependency_injector import containers, providers
from django.conf import settings

from apps.blockchain.application.services.blockchain_service import BlockchainService
from apps.blockchain.application.services.faucet_service import FaucetService
from apps.blockchain.application.services.tx_status_checker_service import TxStatusCheckerService
from infrastructure.repositories.django_faucet_repository import DjangoFaucetTransactionsRepository


class DjangoContainer(containers.DeclarativeContainer):
    # dependencies
    config = providers.Configuration()

    # repositories is stateless, so we can use Singleton
    faucet_repository = providers.Singleton(DjangoFaucetTransactionsRepository)

    # services may be stateful, so we use Factory
    blockchain_service = providers.Factory(
        BlockchainService,
        provider_url=config.BLOCKCHAIN_PROVIDER_URL,
        mnemonic=config.FAUCET_MNEMONIC_KEY,
        chain_id=config.BLOCKCHAIN_CHAIN_ID,
    )

    faucet_service = providers.Factory(
        FaucetService,
        blockchain_service=blockchain_service,
        faucet_transactions_repository=faucet_repository,
        threshold_timeout_minutes=config.FAUCET_THRESHOLD_TIMEOUT_MINUTES,
        amount_eth=config.FAUCET_AMOUNT_ETH,
    )

    tx_status_checker_service = providers.Factory(
        TxStatusCheckerService,
        blockchain_service=blockchain_service,
        faucet_transactions_repository=faucet_repository,
        loop_timeout_seconds=5,  # check for new txs every 5 seconds
    )


def get_app_container():
    """Factory function to create a container with Django settings."""
    container = DjangoContainer()

    # Load settings from Django settings
    container.config.from_dict(
        {
            "BLOCKCHAIN_PROVIDER_URL": settings.BLOCKCHAIN_PROVIDER_URL,
            "BLOCKCHAIN_CHAIN_ID": settings.BLOCKCHAIN_CHAIN_ID,
            "FAUCET_MNEMONIC_KEY": settings.FAUCET_MNEMONIC_KEY,
            "FAUCET_THRESHOLD_TIMEOUT_MINUTES": settings.FAUCET_THRESHOLD_TIMEOUT_MINUTES,
            "FAUCET_AMOUNT_ETH": settings.FAUCET_AMOUNT_ETH,
        }
    )
    return container
