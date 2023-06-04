from django.core.management.base import BaseCommand

from askme.models import Tag

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными тегами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых тегов')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            tag = Tag.objects.create(title=fake.word())
