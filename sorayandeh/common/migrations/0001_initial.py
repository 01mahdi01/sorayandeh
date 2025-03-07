# Generated by Django 4.0.7 on 2025-02-21 04:46

from django.db import migrations, models
import django.db.models.expressions
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RandomModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='randommodel',
            constraint=models.CheckConstraint(check=models.Q(('start_date__lt', django.db.models.expressions.F('end_date'))), name='start_date_before_end_date'),
        ),
    ]
