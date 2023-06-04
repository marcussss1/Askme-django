import json

from django.contrib import auth, messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from askme.paginator import paginate
from askme.models import *
from urllib.parse import urlsplit, urlunsplit
from askme import forms
from Web.settings import CENTRIFUGO_URL, CENTRIFUGO_WS_URL, CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, CENTRIFUGO_API_KEY

# import Faker
# from random import shuffle

import time
import jwt
from cent import Client
from django.forms.models import model_to_dict

client = Client(CENTRIFUGO_URL, api_key=CENTRIFUGO_API_KEY, timeout=1)


def index(request):
    form = {}
    if request.method == 'GET':
        form = forms.SearchForm()
    else:
        form = forms.SearchForm(data=request.POST)
        title = request.POST['title']
        question_list = Question.objects.filter(title__search=title)
        content = paginate(question_list, request)
        content['form_search'] = form
        return render(request, 'index.html', content)

    question_list = Question.objects.new_questions()
    content = paginate(question_list, request)
    content['form_search'] = form
    return render(request, 'index.html', content)

def question(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    comments = Comment.objects.filter(question_id=question_id)

    comments_page = paginate(comments, request)
    # content = {}
    secret_token = {}
    cent_chan = {}
    cent_ws_url = {}

    if request.user.is_authenticated:
        user_id = str(request.user.pk)
        secret_token = jwt.encode({"sub": user_id, "exp": int(time.time()) + 10 * 60},
                                  CENTRIFUGO_TOKEN_HMAC_SECRET_KEY).decode()
        cent_chan = f'question_{question_id}'

    initial = {'question': question.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.profile

    if request.method == 'GET':
        form = forms.CommentForm(initial=initial)
    else:
        form = forms.CommentForm(initial=initial, data=request.POST)
        if form.is_valid():
            comment = form.save()
            if comments_page['current_num_objects'] + 1 > 10:
                page = comments_page['num_pages'] + 1
                comments_page['object_list'].object_list = comment
            else:
                page = comments_page['num_pages']
                comments_page['object_list'] = list(comments_page['object_list'].object_list).append(comment)
            path_to_redirect = question.get_absolute_url() + '?page=%d#%d' % (page, comment.pk)
            client.publish(f"question_{question_id}", model_to_dict(comment))
            return redirect(path_to_redirect, {'question': question, 'comments': comments_page, 'form': form})

    return render(request, 'question.html', {'question': question,
                                             'question_id': question_id,
                                             'comments': comments_page,
                                             'form': form,
                                             'secret_token': secret_token,
                                             'cent_chan': cent_chan,
                                             'cent_ws_url': cent_ws_url,
                                             'flag': False})


def tag(request, tag):
    question_list = Question.objects.tag_questions(tag)

    return render(request, 'index.html', paginate(question_list, request))


def hot(request):
    question_list = Question.objects.best_questions()

    return render(request, 'index.html', paginate(question_list, request))


@login_required
def ask(request):
    if request.method == 'GET':
        form = forms.QuestionForm(request.user.profile)
    else:
        form = forms.QuestionForm(request.user.profile, data=request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question', args=[question.pk]))

    return render(request, 'ask.html', {'form': form})


@login_required
def profile(request):
    user = get_object_or_404(User, username=request.user.username)
    if request.method == 'GET':
        form = forms.ProfileForm(initial={'nickname': user.profile.nickname}, instance=user)
    else:
        form = forms.ProfileForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if key != 'avatar':
                    setattr(user, key, value)
                    setattr(user.profile, key, value)
                if request.FILES.get('avatar') is not None:
                    user.profile.avatar = request.FILES.get('avatar')
            user.save()
            messages.success(request, 'Профиль успешно сохранен', fail_silently=True)
            return redirect('profile')

    return render(request, 'profile.html', {'form': form})


def login(request):
    next = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'GET':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            if form.user is not None:
                auth.login(request, form.user)
                if next and next != request.path:
                    return redirect(request.POST.get('next', reverse('index')))
                return redirect('index')
            else:
                return render(request, 'login.html', {'form': form, 'next': next})

    return render(request, 'login.html', {'form': form, 'next': next})


def logout(request):
    path_to_return = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(path_to_return)


def signup(request):
    if request.method == 'GET':
        form = forms.UserRegistrationForm()
    else:
        form = forms.UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.profile.avatar = request.FILES.get('avatar', None)
            user.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                auth.login(request, user)
                return redirect('index')

    return render(request, 'signup.html', {'form': form})

def ajax_comment(request):
    return redirect('/')
    # return HttpResponseRedirect("/")
    # print(request)
    # question_list = Question.objects.new_questions()
    # return render(request, 'index.html', paginate(question_list, request))
    # print(request.user.profile.nickname)
    # return render(request, 'index.html')

    # return redirect('index')
    # return render(request, f'question.html', {'for'})

    # return redirect(f'question/{request.POST["data[data][question]"]}')

    # text = request.POST['data[data][text]']
    # author_id = request.POST['data[data][author]']
    # question_id = request.POST['data[data][question]']
    #
    # comment = Comment.objects.create(text=text,question=Question.objects.get(id=question_id),author=request.user.profile)
    #                                  # question=Question.objects.get(id=question_id).id)
    #                                  # author=AUTH_PROFILE_MODULE.object)
    # comment.save()
    #
    # return redirect('/')

@login_required
def like(request):
    response_data = {}

    if request.method == 'POST':
        obj_id = int(request.POST.get('id'))
        action = int(request.POST.get('action'))

        obj = Question.objects.get(pk=obj_id)

        new_rating = Like.objects.create(obj, request.user.profile, obj_id, action)

        response_data['new_rating'] = new_rating
        response_data['result'] = 'OK'

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def clike(request):
    response_data = {}

    if request.method == 'POST':
        obj_id = int(request.POST.get('id'))
        action = int(request.POST.get('action'))

        obj = Comment.objects.get(pk=obj_id)

        new_rating = Like.objects.create(obj, request.user.profile, obj_id, action)

        response_data['new_rating'] = new_rating
        response_data['result'] = 'OK'

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def set_right_answ(request):
    response_data = {}

    if request.method == 'POST':
        question = int(request.POST.get('question_id'))
        answer = int(request.POST.get('answer_id'))

        q = Question.objects.get(pk=question)
        a = Comment.objects.get(pk=answer)

        if request.user.profile == q.author:
            if q.id_answer < 0:
                q.id_answer = answer
                a.best_comment = True
                q.save()
                a.save()
                response_data['result'] = 'OK'
            response_data['result'] = 'ANSWER EXISTS'
        else:
            response_data['result'] = 'USER_IS_NOT_AUTHOR'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


def request_params(request):
    content = {'form': forms.ParametersForm()}

    if request.method == 'POST':
        content['form'] = forms.ParametersForm(data=request.POST)
        if content['form'].is_valid():
            content['POST'] = request.POST.dict()

    if request.method == 'GET':
        content['GET'] = request.GET.dict()

    return render(request, 'utils/parameters.html', content)
