from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset migration dependencies for AT Identity'
    
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Remove problematic migration records
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = 'at_identity'"
            )
            self.stdout.write('Cleared AT Identity migration records')
            
            # Reset admin migration dependency if needed
            cursor.execute(
                "UPDATE django_migrations SET applied = NOW() WHERE app = 'admin' AND name = '0001_initial'"
            )
            
        self.stdout.write(self.style.SUCCESS('Migration dependencies reset'))