# Generated by Django 5.0.2 on 2025-03-01 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0004_alter_campaign_steel_needed_money_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="steel_needed_money",
            field=models.IntegerField(default=0, verbose_name="Estimated Money"),
        ),
    ]
