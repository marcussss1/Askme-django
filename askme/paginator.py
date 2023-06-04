from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from askme.models import Profile
from django.core.cache import cache

from random import shuffle
import time

def get_user_rating():
    lst = list(range(1, 4))
    shuffle(lst)
    time.sleep(5)
    users = []
    for i in lst:
        users.append(Profile.objects.get(id=i))
    return users

def calculate_rating():
    # users = Profile.get_top_users(10)
    users = get_user_rating()
    cache.set('rating', users, 70)

def prepare_context(content):
    return {'top_users': cache.get('rating')}

def paginate(objects_list, request):
    context = {}

    # Создание пагинатора
    current_page = Paginator(objects_list, 10)
    page = request.GET.get('page')

    try:
        # Если существует, то выбираем эту страницу
        context['object_list'] = current_page.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        context['object_list'] = current_page.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        context['object_list'] = current_page.page(current_page.num_pages)

    # количество страниц слева и справа от текущей
    ADD_PAGES = 3

    if context['object_list'].paginator.num_pages > ADD_PAGES * 2 + 1:
        # количество страниц больше чем "окно"

        # найдем начало и конец "окна" для общего случая
        start_window = context['object_list'].number - ADD_PAGES
        end_window = context['object_list'].number + ADD_PAGES

        if start_window < 1:
            # если "окно вылезает" за левую границу
            # то левую границу ставим на 1-ю страницу
            start_window = 1
            # а правую границу вычисляем относительно 1-й
            end_window = 1 + ADD_PAGES * 2

        if end_window > context['object_list'].paginator.num_pages:
            # если "окно вылезает" за правую границу
            # то правую границу ставим на последнюю страницу
            end_window = context['object_list'].paginator.num_pages
            # а левую границу вычисляем относительно последней страницы
            start_window = end_window - ADD_PAGES * 2

        # определим итератор для "окна"
        my_page_range = range(start_window, end_window + 1)

    else:
        # количество страниц меньше или равно "окну"
        # просто используем весь диапазон доступных страниц, т.е. page_range
        my_page_range = context['object_list'].paginator.page_range

    context['page_range'] = my_page_range
    context['num_pages'] = current_page.num_pages
    context['current_num_objects'] = len(current_page.page(current_page.num_pages))
    prepare_context(context)
    return context
