# Generated by Django 3.0 on 2019-12-14 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgchart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='id',
        ),
        migrations.AddField(
            model_name='company',
            name='company_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='person_id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
