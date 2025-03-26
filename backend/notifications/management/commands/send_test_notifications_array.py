from django.core.management.base import BaseCommand
from notifications.utils import send_notification


class Command(BaseCommand):
    help = "Send a test notification to multiple Django users at once."

    def add_arguments(self, parser):
        parser.add_argument(
            "user_ids", 
            type=str, 
            help="Comma-separated list of Django user IDs (e.g. '1,2,3')"
        )
        parser.add_argument(
            "--title", 
            type=str, 
            default="Test Multiple Users Notification"
        )
        parser.add_argument(
            "--message", 
            type=str, 
            default="This is a test notification sent to multiple users."
        )

    def handle(self, *args, **options):
        user_ids_str = options["user_ids"]
        title = options["title"]
        message = options["message"]
        
        # Parse the comma-separated list into a list of integers
        user_ids = [int(user_id.strip()) for user_id in user_ids_str.split(',') if user_id.strip()]

        if not user_ids:
            self.stdout.write(self.style.ERROR("No valid user IDs provided. Please use comma-separated IDs (e.g. '1,2,3')"))
            return

        self.stdout.write(f"Attempting to send notification to user IDs: {user_ids}")
        
        success = send_notification(
            title=title,
            message=message,
            django_user_ids=user_ids
        )

        if success:
            self.stdout.write(
                self.style.SUCCESS(f"Notification successfully queued for Django user IDs: {user_ids}")
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"Failed to queue notification for Django user IDs: {user_ids}")
            ) 