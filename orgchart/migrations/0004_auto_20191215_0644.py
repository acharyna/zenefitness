# Generated by Django 3.0 on 2019-12-15 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgchart', '0003_auto_20191215_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='department_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='manager_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='work_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
