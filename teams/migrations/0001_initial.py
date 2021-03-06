# Generated by Django 3.1.3 on 2020-11-11 09:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='チーム名')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, verbose_name='名前')),
                ('student_number', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator('^\\d{7}$', '正しい学籍番号を入力してください')], verbose_name='学籍番号')),
                ('join_date', models.DateField(null=True, verbose_name='チーム加入日')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
        ),
    ]
