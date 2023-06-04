from django.core.management.base import BaseCommand

import random
from faker import Faker

fake = Faker()

from askme.models import *


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными комментами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых комментов')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = Profile.objects.values_list('id', flat=True)
        questions_list = Question.objects.values_list('id', flat=True)

        for i in range(total):
            a = random.choice(author_list)
            q = random.choice(questions_list)
            com = Comment.objects.create(text=fake.text(), question_id=q, author_id=a)
