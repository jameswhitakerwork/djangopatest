# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 04:19
from __future__ import unicode_literals

from django.db import migrations
import jsignature.fields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='signature',
            field=jsignature.fields.JSignatureField(default=None),
            preserve_default=False,
        ),
    ]