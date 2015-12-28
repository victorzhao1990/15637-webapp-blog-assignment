from django.db import models
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import escape


# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=50, default="", blank=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s %s' % (self.content, self.dateTime, self.author)

    @staticmethod
    def get_posts(author):
        return Post.objects.filter(author=author)\
            .order_by("dateTime").reverse()

    @staticmethod
    def get_all_posts(logentry_id=-1):
        return Post.objects.filter(deleted=False, logentry__gt=logentry_id).distinct()

    @staticmethod
    def get_changes(logentry_id=-1):
        return Post.objects.filter(logentry__gt=logentry_id).distinct()

    @property
    def html(self):
        return "<li class='post_item' id='post_%d'> <div class='blog-post'> <p class='blog-post-meta'> %s by <a href='/grumblr/profile/%s'>%s %s</a> <img src='/grumblr/photo/%s' alt='%s' width='50' height='50'> </p> <p>%s</p> </div> <div class='dropdown'><button class='btn btn-primary dropdown-toggle' type='button' data-toggle='dropdown'>Comment<span class='caret'></span></button><ul class='dropdown-menu'></ul></div> </li>" % (self.id, self.dateTime, escape(self.author.username), escape(self.author.first_name), escape(self.author.last_name), escape(self.author.username), escape(self.author.username), escape(self.content))


class LogEntry(models.Model):
    post = models.ForeignKey(Post)
    op = models.CharField(max_length=3, choices=[('add', 'add'), ('del', 'del')])

    def __unicode__(self):
        return "LogEntry (%d, %s, %s)" % (self.id, self.post, self.op)

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_max_id():
        return LogEntry.objects.all().aggregate(Max('id'))['id__max'] or 0


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.CharField(max_length=50, default="", blank=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s %s %s' % (self.post, self.content, self.dateTime, self.author)

    @staticmethod
    def get_comments(post, logcommentry_id=-1):
        # return Post.objects.filter(author=author)\
        #     .order_by("dateTime").reverse()
        return Comment.objects.filter(deleted=False, logcommentry__gt=logcommentry_id, post=post).distinct().reverse()


    @staticmethod
    def get_changes(post, logcommentry_id=-1):
        return Comment.objects.filter(post=post, logcommentry__gt=logcommentry_id).distinct().reverse()

    @property
    def html(self):
        # TODO: need to change to correspond format
        # Hope it will work
        return "<li id='comment_%d'> <div> <p> %s by <a href='/grumblr/profile/%s'>%s %s</a> <img src='grumblr/photo/%s' alt='%s' width='25' height='25'> </p> <p>%s</p> </div> </li>" % (self.id, self.dateTime, escape(self.author.username), escape(self.author.first_name), escape(self.author.last_name), escape(self.author.username), escape(self.author.username), escape(self.content))


class LogCommEntry(models.Model):
    comment = models.ForeignKey(Comment)
    op = models.CharField(max_length=3, choices=[('add', 'add'), ('del', 'del')])

    def __unicode__(self):
        return "LogCommEntry (%d, %s, %s)" % (self.id, self.comment, self.op)

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_max_id():
        return LogCommEntry.objects.all().aggregate(Max('id'))['id__max'] or 0




class Profile(models.Model):
    password1 = models.CharField(max_length=100, default="", blank=True)
    password2 = models.CharField(max_length=100, default="", blank=True)
    first_name = models.CharField(max_length=30, default="", blank=True)
    last_name = models.CharField(max_length=30, default="", blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    age = models.IntegerField(default=18, blank=True)
    short_bio = models.CharField(max_length=420, default="", blank=True)
    image = models.ImageField(upload_to="profile-photos", )

    followers = models.ManyToManyField(User, related_name='f+')

    @staticmethod
    def get_followers(username):
        return Profile.objects.get(user=User.objects.get(username=username)).followers.all()


