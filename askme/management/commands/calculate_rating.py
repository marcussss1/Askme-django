from django.core.management.base import BaseCommand

from askme.paginator import calculate_rating

class Command(BaseCommand):

    def handle(self, *args, **options):
        calculate_rating()