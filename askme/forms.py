import os
from django.template.defaultfilters import filesizeformat
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from askme.models import Question, Comment
from PIL import Image, ImageFilter


# --------------------------------------------- AVATAR VALIDATOR ---------------------------------------------
def size(img):
    max = 50 * 1024
    if img.size > max:
        raise forms.ValidationError('Файл слишком большой (%s). Максимальный размер файла - %s' %
                                    (filesizeformat(img.size), filesizeformat(max)))


# --------------------------------------------- LOGIN ---------------------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError('Имя пользователя содержит пробелы')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такого пользователя не существует')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if ' ' in password:
            raise forms.ValidationError('Пароль содержит пробелы')
        return password

    def clean(self):
        cdata = super().clean()
        username = cdata.get('username')
        password = cdata.get('password')

        if username and password:
            if not self.errors:
                user = authenticate(username=username, password=password)
                if user is None:
                    errors = {'password': ValidationError('Введен неверный пароль')}
                    raise ValidationError(errors)
                self.user = user

        return cdata


# --------------------------------------------- REGISTER ---------------------------------------------
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.EmailField()
    nickname = forms.CharField(label="Никнейм")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
    avatar = forms.ImageField(label="Загрузить аватар", required=False, validators=[size])

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if ' ' in nickname:
            raise forms.ValidationError('Никнейм содержит пробелы')
        return nickname

    def clean_password2(self):
        password2 = self.cleaned_data['password2']
        if not password2:
            raise forms.ValidationError('Введите пароль повторно')
        return password2

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if ' ' in password1:
            errors = {'password1': ValidationError('Пароль содержит пробелы')}
            raise forms.ValidationError(errors)

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают'),
                      'password1': ValidationError('')}
            raise ValidationError(errors)

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password1', 'password2', 'avatar')


# --------------------------------------------- ASK ---------------------------------------------
class TagsFieldWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={'placeholder': 'Введите тэги через запятую'})]
        super(TagsFieldWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value]
        else:
            return ['']


class TagsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = [forms.CharField()]
        super(TagsField, self).__init__(fields, widget=TagsFieldWidget, *args, **kwargs)

    def compress(self, values):
        return values[0]


class QuestionForm(forms.ModelForm):
    tags = TagsField(label='Тэги')

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']
        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(attrs={'placeholder': 'Введите ваш вопрос', 'rows': 10}),
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        lst = tags.split(', ', maxsplit=3)
        if len(lst) > 3:
            raise forms.ValidationError('Пост должен содержать не более трех тэгов')
        for tag in lst:
            if ' ' in tag:
                raise forms.ValidationError('Тэг содержит пробел')
        return lst

    def __init__(self, author, *args, **kwargs):
        self.author = author
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        question = Question(title=self.cleaned_data['title'], text=self.cleaned_data['text'])
        question.author = self.author
        if commit:
            question.save()
            for tag in self.cleaned_data['tags']:
                question.add_tag(tag)
            question.save()
        return question


# --------------------------------------------- COMMENT ---------------------------------------------
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'question', 'author']
        widgets = {
            'question': forms.HiddenInput,
            'author': forms.HiddenInput,
            'text': forms.Textarea(attrs={'placeholder': 'Введите ваш комментарий', 'rows': 4})
        }

    def save(self, commit=True):
        comment = Comment(**self.cleaned_data)
        if commit:
            comment.save()
        return comment


# --------------------------------------------- PROFILE ---------------------------------------------
class ProfileForm(forms.ModelForm):
    email = forms.EmailField()
    nickname = forms.CharField(label="Никнейм")
    avatar = forms.ImageField(label="Аватар", required=False, validators=[size])

    # def __init__(self, request_user, *args, **kwargs):
    #   self.request_user = request_user
    #   super().__init__(*args, **kwargs)

    def clean_nickname(self):
        username = self.cleaned_data['nickname']
        if ' ' in username:
            raise forms.ValidationError('Никнейм содержит пробелы')
        return username

    class Meta:
        model = User
        fields = ['email', 'nickname', 'avatar']


# --------------------------------------------- GET/POST PARAMS ---------------------------------------------
class ParametersForm(forms.Form):
    param = forms.CharField(label="POST-параметр", widget=forms.TextInput, required=False)

class SearchForm(forms.Form):
    title = forms.CharField(label='Заголовок вопроса', widget=forms.TextInput)
