# Generated by Django 5.1.2 on 2024-10-22 12:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_contributed', models.DecimalField(decimal_places=2, max_digits=5)),
                ('contribution_date', models.DateField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer_records', to='projects.project')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='volunteer_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'volunteer_records',
            },
        ),
    ]
