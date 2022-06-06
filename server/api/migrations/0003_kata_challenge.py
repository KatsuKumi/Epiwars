# Generated by Django 4.0.4 on 2022-06-02 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('test_script', models.TextField()),
                ('test_example', models.TextField()),
                ('description', models.TextField()),
                ('starter_code', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('first_kata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='first_kata', to='api.kata')),
                ('katas', models.ManyToManyField(to='api.kata')),
            ],
        ),
    ]