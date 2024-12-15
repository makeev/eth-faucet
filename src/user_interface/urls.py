from django.urls import path

from user_interface.views import FundWalletView, StatsView

urlpatterns = [
    path("faucet/fund", FundWalletView.as_view()),
    path("faucet/stats", StatsView.as_view()),
]
