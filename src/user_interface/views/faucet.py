from rest_framework import serializers, status
from rest_framework.views import APIView

from apps.blockchain.application.dto import FaucetTransactionDTO
from base.serializers import BaseSerializer
from infrastructure.container import get_app_container
from user_interface.utils import extend_schema

from ..response import TypedResponse

app_container = get_app_container()


class InputParamsSerializer(BaseSerializer):
    """We usig serializers for input parameters validation only"""

    wallet_address = serializers.CharField(max_length=42)


class FundWalletView(APIView):
    def _get_ip_address(self, request):
        # TODO: Implement a better way to get the IP address
        return request.META.get("REMOTE_ADDR")

    @extend_schema(request=InputParamsSerializer, responses={201: FaucetTransactionDTO})
    def post(self, request) -> TypedResponse[FaucetTransactionDTO]:
        serializer = InputParamsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ip_address = self._get_ip_address(request)

        transaction_dto = app_container.faucet_service().fund_wallet(
            serializer.validated_data["wallet_address"],  # type: ignore
            ip_address,
        )
        return TypedResponse(transaction_dto, status=status.HTTP_201_CREATED)


# class StatsView(APIView):
#     def get(self, request):
#         faucet_transactions_repository = DjangoDaucetRepository()

#         # Fetch statistics for the last 24 hours
#         stats = faucet_transactions_repository.get_statistics(last_hours=24)

#         return Response(stats, status=status.HTTP_200_OK)
