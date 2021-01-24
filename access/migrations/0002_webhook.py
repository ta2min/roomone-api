# Generated by Django 3.1.3 on 2020-12-28 02:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_member_owner'),
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Slack'), (2, 'Teams')])),
                ('url', models.URLField(unique=True, verbose_name='webhookのURL')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
        ),
    ]