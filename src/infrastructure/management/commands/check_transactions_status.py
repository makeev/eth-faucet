from django.core.management.base import BaseCommand

from infrastructure.container import get_app_container

app_container = get_app_container()


class Command(BaseCommand):
    help = "Set statuses to transactions"

    def handle(self, *args, **options):
        try:
            app_container.tx_status_checker_service().run()
        except KeyboardInterrupt:
            app_container.tx_status_checker_service().stop()
            self.stdout.write(self.style.SUCCESS("TxStatusCheckerService stopped"))
