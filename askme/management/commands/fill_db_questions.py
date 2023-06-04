from django.core.management.base import BaseCommand
import random

from askme.models import *

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными вопросами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых постов')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = Profile.objects.values_list('id', flat=True)
        tag_list = Tag.objects.values_list('id', flat=True)

        for i in range(total):
            q = Question.objects.create(title=fake.sentence(),
                                        text=fake.text()[:500],
                                        author_id=random.choice(author_list))

            for x in range(random.randint(1, 3)):
                t = random.choice(tag_list)
                q.tags.add(t)
