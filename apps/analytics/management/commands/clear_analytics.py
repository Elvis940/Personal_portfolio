from django.core.management.base import BaseCommand
from apps.analytics.models import AnalyticsEvent


class Command(BaseCommand):
    help = 'Clear all analytics data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompt',
        )

    def handle(self, *args, **options):
        count = AnalyticsEvent.objects.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No analytics data to clear.'))
            return
        
        if not options.get('confirm'):
            confirm = input(f'Are you sure you want to delete {count} analytics events? (y/n): ')
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return
        
        AnalyticsEvent.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully cleared {count} analytics events.'))