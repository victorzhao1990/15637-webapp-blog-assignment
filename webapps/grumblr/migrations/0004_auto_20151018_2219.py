# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0003_post_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logentry',
            name='post',
        ),
        migrations.DeleteModel(
            name='LogEntry',
        ),
    ]
