# Generated by Django 3.0.3 on 2020-02-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20200216_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
                ('username', models.CharField(default='', max_length=30)),
                ('email', models.CharField(default='', max_length=30)),
                ('password', models.CharField(default='', max_length=30)),
                ('date', models.CharField(default='', max_length=10)),
                ('time', models.CharField(default='', max_length=10)),
            ],
        ),
    ]
