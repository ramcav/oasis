from django.core.management.base import BaseCommand
from notifications.utils import send_notification  # adjust path as necessary

class Command(BaseCommand):
    help = "Send a test notification to a Django user."

    def add_arguments(self, parser):
        parser.add_argument("django_user_id", type=str)
        parser.add_argument("--title", type=str, default="Test Notification")
        parser.add_argument("--message", type=str, default="This is a test notification.")

    def handle(self, *args, **options):
        django_user_id = options["django_user_id"]
        title = options["title"]
        message = options["message"]

        success = send_notification(
            title=title,
            message=message,
            django_user_ids=[django_user_id]
        )

        if success:
            self.stdout.write(self.style.SUCCESS(f"Notification successfully queued for Django user ID: {django_user_id}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to queue notification for Django user ID: {django_user_id}"))
