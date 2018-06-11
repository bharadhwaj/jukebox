# Generated by Django 2.0.6 on 2018-06-08 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('publish_date', models.DateTimeField(auto_now_add=True, verbose_name='date added')),
            ],
        ),
    ]
