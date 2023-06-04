from django.conf import settings as djsettings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, upload_to='uploads/')
    nickname = models.CharField(max_length=30)

    def get_top_users(count):
        # count = min(count, Profile.object.count())
        users = Profile.objects.all()
        return users

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return djsettings.STATIC_URL + 'img/default_avatar.svg'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    title = models.CharField(max_length=30, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('tag', args=[self.title])

    def __str__(self):
        return self.title


class LikeManager(models.Manager):
    use_for_related_fields = True

    def like_sort(self, user, id, type):
        return self.get_queryset().filter(vote__gt=0, user=user, object_id=id, content_type__model=type)

    def dislike_sort(self, user, id, type):
        return self.get_queryset().filter(vote__lt=0, user=user, object_id=id, content_type__model=type)

    def create(self, target, user, pk, vote_type):
        obj = target.__class__.objects.get(pk=pk)
        try:
            like = Like.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=user)
            if like.vote is not vote_type:
                obj.rating -= like.vote
                like.vote = vote_type
                obj.rating += like.vote
                obj.save(update_fields=['rating'])
                like.save(update_fields=['vote'])
            else:
                obj.rating -= like.vote
                like.delete()
                obj.save(update_fields=['rating'])
        except Like.DoesNotExist:
            obj.votes.create(user=user, vote=vote_type)
            obj.rating += vote_type
            obj.save(update_fields=['rating'])

        return obj.rating


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(choices=VOTES)

    user = models.ForeignKey(djsettings.AUTH_PROFILE_MODULE, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeManager()

    def __str__(self):
        title = str(self.user) + " votes " + str(self.object_id) + " by " + str(self.vote) + " | " + str(self.content_type.name)
        return title


class QuestionManager(models.Manager):
    def best_questions(self):
        return self.get_queryset().order_by('-rating').annotate(comment_count=Count('comment'))

    def new_questions(self):
        return self.get_queryset().order_by('-creating_date').annotate(comment_count=Count('comment'))

    def tag_questions(self, tag):
        return self.get_queryset().filter(tags__title__contains=tag).annotate(comment_count=Count('comment'))


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    creating_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    author = models.ForeignKey(djsettings.AUTH_PROFILE_MODULE, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    votes = GenericRelation(Like, related_query_name='questions')

    rating = models.IntegerField(default=0)
    id_answer = models.IntegerField(default=-1)

    objects = QuestionManager()

    class Meta:
        ordering = ['-creating_date']

    def add_tag(self, tag):
        tag, created = Tag.objects.get_or_create(title=tag)
        self.tags.add(tag.id)
        self.save()

    def get_absolute_url(self):
        return reverse('question', args=[self.pk])

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    best_comment = models.BooleanField(default=False)
    creating_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(djsettings.AUTH_PROFILE_MODULE, on_delete=models.CASCADE)
    votes = GenericRelation(Like, related_query_name='comments')

    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text
