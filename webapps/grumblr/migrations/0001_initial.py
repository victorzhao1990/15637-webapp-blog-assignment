# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op', models.CharField(max_length=3, choices=[(b'add', b'add'), (b'del', b'del')])),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'', max_length=50, blank=True)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password1', models.CharField(default=b'', max_length=100, blank=True)),
                ('password2', models.CharField(default=b'', max_length=100, blank=True)),
                ('first_name', models.CharField(default=b'', max_length=30, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=30, blank=True)),
                ('age', models.IntegerField(default=18, blank=True)),
                ('short_bio', models.CharField(default=b'', max_length=420, blank=True)),
                ('image', models.ImageField(upload_to=b'profile-photos')),
                ('followers', models.ManyToManyField(related_name='f+', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='logentry',
            name='post',
            field=models.ForeignKey(to='grumblr.Post'),
        ),
    ]
