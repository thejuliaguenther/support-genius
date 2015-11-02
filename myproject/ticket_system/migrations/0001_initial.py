# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('password', models.CharField(max_length=50, blank=True)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('tier', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('domain', models.CharField(max_length=50, blank=True)),
                ('location', models.CharField(max_length=50, blank=True)),
                ('time_zone', models.CharField(max_length=100, blank=True)),
                ('industry', models.CharField(max_length=50, blank=True)),
                ('support_tier', models.CharField(max_length=50, blank=True)),
                ('is_pilot', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('phone_number', models.CharField(max_length=50, blank=True)),
                ('job_title', models.CharField(max_length=50, blank=True)),
                ('company_id', models.ForeignKey(to='ticket_system.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_id', models.AutoField(serialize=False, primary_key=True)),
                ('channel_submitted', models.CharField(max_length=50, blank=True)),
                ('ticket_content', models.CharField(max_length=500)),
                ('time_submitted', models.DateTimeField()),
                ('num_agent_touches', models.IntegerField()),
                ('time_first_responded', models.DateTimeField()),
                ('agent_id', models.ForeignKey(to='ticket_system.Agent')),
                ('customer_id', models.ForeignKey(to='ticket_system.Customer')),
            ],
        ),
    ]
