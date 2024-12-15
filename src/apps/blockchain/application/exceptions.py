from apps.blockchain.domain.value_objects import IPAddress, WalletAddress
from base.exceptions import BaseResponseError


class TooManyTransactionsFromIpError(BaseResponseError):
    code = 429

    def __init__(self, ip: IPAddress):
        self.ip = ip
        self.message = f"Too many transactions from IP {ip.value}"
        super().__init__(self.message)


class TooManyTransactionsFromWalletError(BaseResponseError):
    code = 429

    def __init__(self, wallet: WalletAddress):
        self.wallet = wallet
        self.message = f"Too many transactions from wallet {wallet.value}"
        super().__init__(self.message)


class UndefinedError(BaseResponseError):
    code = 500

    def __init__(self, error: Exception):
        self.error = error
        self.message = f"Undefined error: {error}"
        super().__init__(self.message)
