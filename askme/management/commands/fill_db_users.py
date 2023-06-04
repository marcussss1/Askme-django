from django.core.management.base import BaseCommand

from askme.models import User

from faker import Faker

f = Faker()


class Command(BaseCommand):
    help = u'Заполнение базы данных случайными юзерами'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help=u'Количество создаваемых пользователей')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            user = User.objects.create_user(username=f.name(),
                                            email=f.email(),
                                            password='12345')
            user.profile.nickname = f.last_name()
            user.profile.save()
