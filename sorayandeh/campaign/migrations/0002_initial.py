# Generated by Django 4.0.7 on 2024-11-05 00:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('applicant', '0001_initial'),
        ('campaign', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='participants',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='category',
            field=models.ManyToManyField(related_name='campaign_categories', to='campaign.campaigncategory'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='participants',
            field=models.ManyToManyField(related_name='campaigns_participated', through='campaign.Participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campaign',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.school'),
        ),
    ]
