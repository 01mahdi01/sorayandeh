# Generated by Django 4.0.7 on 2024-11-21 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='category',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='requests',
        ),
        migrations.RenameModel(
            old_name='CampaignCategory',
            new_name='RequestCategory',
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_list', to='campaign.campaign')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_categories', to='campaign.requestcategory')),
            ],
        ),
    ]
