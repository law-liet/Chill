# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Type', models.CharField(max_length=8192)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=8192)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('fb_token', models.CharField(max_length=128)),
                ('fb_id', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('is_chilled', models.BooleanField(default=False)),
                ('Type', models.CharField(default=b'Chilled', max_length=128)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='Main.User')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(to='Main.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='chiller',
            field=models.ForeignKey(related_name='chiller', to='Main.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='members', to='Main.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='messages',
            field=models.ManyToManyField(related_name='messages', to='Main.Message'),
        ),
    ]
