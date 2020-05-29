# Generated by Django 3.0.6 on 2020-05-27 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweet', '0002_tweet_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed', models.BooleanField(default=False)),
                ('tweet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tweet_id', to='tweet.Tweet')),
                ('victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='victim', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
