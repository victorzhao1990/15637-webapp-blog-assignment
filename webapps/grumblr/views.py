from datetime import datetime
from forms import *
from models import *
from mimetypes import guess_type

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@login_required
def home(request):
    # full_name = request.user.get_full_name()
    # post_list = Post.objects.all().order_by("dateTime").reverse()
    # return render(request, 'grumblr/globalstream.html', {'full_name': full_name, 'post_list': post_list})
    return render(request, 'grumblr/globalstream.html')


@login_required
def get_comments(request, post_id, log_id=-1):

    max_logentry = LogCommEntry.get_max_id()
    post = Post.objects.get(id=post_id)
    comments = Comment.get_comments(post=post, logcommentry_id=log_id)
    context = {"max_entry": max_logentry, "comments": comments}

    return render(request, 'comments.json', context, content_type='application/json')


@login_required
def get_comment_changes(request, post_id, log_id=-1):
    print post_id
    max_logentry = LogCommEntry.get_max_id()
    post = Post.objects.get(id=post_id)
    comments = Comment.get_changes(post, log_id)
    print comments

    context = {"max_entry": max_logentry, "comments": comments}

    return render(request, 'comments.json', context, content_type='application/json')



@login_required
def add_comment(request, post_id):
    if not 'content' in request.POST or not request.POST['content']:
        print "44444"
        raise Http404
    else:
        content = request.POST['content']
        author = User.objects.get(username=request.user.get_username())
        post = Post.objects.get(id=post_id)
        comment = Comment(post=post, content=content, dateTime=datetime.now(), author=author)
        comment.save()

        log_comm_entry = LogCommEntry(comment=comment, op='add')
        log_comm_entry.save()

    return HttpResponse("")


@login_required
def add_post(request):
    if not 'content' in request.POST or not request.POST['content']:
        raise Http404
    else:
        content = request.POST['content']
        author = User.objects.get(username=request.user.get_username())
        post = Post(content=content, dateTime=datetime.now(), author=author)
        post.save()

        log_entry = LogEntry(post=post, op='add')
        log_entry.save()

    return HttpResponse("")


@login_required
def get_posts(request, username="", log_id=-1):
    print "**********"
    max_logentry = LogEntry.get_max_id()
    print max_logentry, "sb"
    posts = Post.get_all_posts(log_id)
    if username != "":
        u = User.objects.get(username=username)
        posts = Post.get_posts(author=u)
    context = {"max_entry": max_logentry, "posts": posts}
    for post in posts:
        print post.html
    print "******"
    return render(request, 'posts.json', context, content_type='application/json')


@login_required
def get_changes(request, log_id=-1):
    print "*********"
    max_logentry = LogEntry.get_max_id()
    posts = Post.get_changes(log_id)

    context = {"max_entry": max_logentry, "posts": posts}
    return render(request, 'posts.json', context, content_type='application/json')


@transaction.atomic
def registration(request):

    context = {}

    if request.method == 'GET':
        context['form'] = UserForm()
        return render(request, 'grumblr/signup.html', context)

    form = UserForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        print form
        return render(request, 'grumblr/signup.html', context)

    data = form.cleaned_data

    new_user = User.objects.create_user(username=data['username'], email=data['email'],
                                        password=data['password1'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])
    new_user.save()

    p = Profile.objects.create(user=User.objects.get(username=data['username']))
    p.save()

    new_user = authenticate(username=data['username'], password=data['password1'])

    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def profile(request, username=""):
    context = {}

    if username == "":
        username = request.user.username
    curr_user = username
    print curr_user

    try:
        userInfo = User.objects.get(username=curr_user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/grumblr/profile/')
    full_name = userInfo.get_full_name()
    first_name = userInfo.get_short_name()
    post_list = Post.objects.filter(author=userInfo).order_by("dateTime").reverse()
    age = Profile.objects.get(user=userInfo).age
    short_bio = Profile.objects.get(user=userInfo).short_bio
    context['fullName'] = full_name
    context['firstName'] = first_name
    context['post_list'] = post_list
    context['targetUsername'] = username
    context['age'] = age
    context['short_bio'] = short_bio
    if curr_user == request.user.username:
        context['edit_profile'] = curr_user
    else:
        if User.objects.get(username=curr_user) in Profile.get_followers(request.user.username):
            context['unfollow'] = curr_user
        else:
            context['follow'] = curr_user

    return render(request, 'grumblr/profile.html'
                  , context,)


@login_required
def new_post(request):
    if request.POST.__contains__('content'):
        content = request.POST['content']
        author = User.objects.get(username=request.user.get_username())
        post = Post(content=content, dateTime=datetime.now(), author=author)
        post.save()
    return HttpResponseRedirect('/grumblr/globalstream/')


@login_required
@transaction.atomic
def profile_edit(request):
    context = {}
    if request.method == 'GET':
        form = ProfileEditForm(instance=Profile.objects.get(user=User.objects.get(username=request.user.username)))
        context['form'] = form
        return render(request, 'grumblr/edit_profile.html', context)

    form = ProfileEditForm(request.POST, request.FILES,
                           instance=Profile.objects.get(user=User.objects.get(username=request.user.username)))

    print form['image']
    if not form.is_valid():
        context = {'form': form}
        return render(request, 'grumblr/edit_profile.html', context)

    form.save()

    context['form'] = form

    data = form.cleaned_data
    print data

    first_name = data['first_name']
    last_name = data['last_name']
    password = data['password1']

    u = User.objects.get(username=request.user.username)
    u.set_password(password)
    u.first_name = first_name
    u.last_name = last_name
    u.save()

    new_user = authenticate(username=request.user.username, password=password)

    login(request, new_user)

    return render(request, 'grumblr/edit_profile.html', context)


@login_required
def get_photo(request, username):
    p = get_object_or_404(Profile, user=User.objects.get(username=username))
    if not p.image:
        raise Http404

    content_type = guess_type(p.image.name)

    return HttpResponse(p.image, content_type=content_type)


@login_required
def follower_list(request):
    followers = Profile.get_followers(request.user.username)

    f_list = []
    for follower in followers:
        print follower.get_username()
        f_list.append(follower.get_username())

    f_json = {'followers': f_list}
    # context = {'followers': f_list}
    return JsonResponse(f_json)

    # print context
    # print "$$$$$$$$$$"
    # return render(request, 'f_list.json', context, content_type='application/json')


@login_required
def follower_stream(request):
    context = {}
    print Profile.get_followers(request.user.username)
    followers = Profile.get_followers(request.user.username)

    post_list = []
    for follower in followers:
        posts = Post.get_posts(follower)
        if len(posts) != 0:
            post_list.extend(posts)

    new_list = sorted(post_list, key=lambda x: x.dateTime, reverse=True)
    context['post_list'] = new_list
    return render(request, 'grumblr/follower-stream.html', context)


@login_required
def follow(request):
    context = {}
    target = request.POST['target']
    p = Profile.objects.get(user=User.objects.get(username=request.user.username))

    target_user = User.objects.get(username=target)
    if request.POST['type'] == "follow":
        if target_user not in Profile.get_followers(request.user.username):
            p.followers.add(target_user)
            p.save()
            context['unfollow'] = target
    elif request.POST['type'] == "unfollow":
        if target_user in Profile.get_followers(request.user.username):
            p.followers.remove(target_user)
            p.save()
            context['follow'] = target

    return HttpResponseRedirect('/grumblr/profile/' + target)







