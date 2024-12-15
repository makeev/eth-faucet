from dataclasses import dataclass

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_dataclasses.serializers import DataclassSerializer

from apps.blockchain.application.dto import FaucetStatsDTO, FaucetTransactionDTO
from infrastructure.container import get_app_container
from user_interface.utils import extend_schema

from ..response import TypedResponse

app_container = get_app_container()


@dataclass
class RequestParams:
    wallet_address: str


class FundWalletView(APIView):
    def _get_ip_address(self, request):
        # TODO: Implement a better way to get the IP address
        return request.META.get("REMOTE_ADDR")

    @extend_schema(request=RequestParams, responses={201: FaucetTransactionDTO})
    def post(self, request) -> TypedResponse[FaucetTransactionDTO]:
        serializer: DataclassSerializer[RequestParams] = DataclassSerializer(data=request.data, dataclass=RequestParams)  # type: ignore
        serializer.is_valid(raise_exception=True)

        transaction_dto = app_container.faucet_service().fund_wallet(
            serializer.validated_data.wallet_address,
            self._get_ip_address(request),
        )
        return TypedResponse(transaction_dto, status=status.HTTP_201_CREATED)


class StatsView(APIView):
    @extend_schema(responses={200: FaucetStatsDTO})
    def get(self, request) -> TypedResponse[FaucetStatsDTO]:
        # Fetch statistics for the last 24 hours
        stats = app_container.faucet_service().get_stats()

        return TypedResponse(stats, status=status.HTTP_200_OK)
