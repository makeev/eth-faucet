from django.urls import path

from user_interface.views import FundWalletView

urlpatterns = [
    # ... existing URL patterns ...
    path("faucet/fund", FundWalletView.as_view(), name="faucet_fund"),
    # path('faucet/stats', StatsView.as_view(), name='faucet_stats'),
]
