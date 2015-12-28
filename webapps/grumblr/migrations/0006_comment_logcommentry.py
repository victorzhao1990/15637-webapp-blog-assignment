# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grumblr', '0005_logentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(default=b'', max_length=50, blank=True)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(to='grumblr.Post')),
            ],
        ),
        migrations.CreateModel(
            name='LogCommEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('op', models.CharField(max_length=3, choices=[(b'add', b'add'), (b'del', b'del')])),
                ('comment', models.ForeignKey(to='grumblr.Comment')),
            ],
        ),
    ]
