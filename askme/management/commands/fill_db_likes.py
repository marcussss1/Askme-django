import random

from django.core.management.base import BaseCommand

from askme.models import *


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными лайкосами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых лайков')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        author_list = User.objects.all()
        questions_list = Question.objects.all()
        comments_list = Comment.objects.all()
        votes = [1, -1]

        for i in range(total):
            a = random.choice(author_list)
            q = random.choice(questions_list)
            c = random.choice(comments_list)

            like_q = Like.objects.create(target=q, user=a.profile, pk=q.id, vote_type=random.choice(votes))
            like_c = Like.objects.create(target=c, user=a.profile, pk=c.id, vote_type=random.choice(votes))