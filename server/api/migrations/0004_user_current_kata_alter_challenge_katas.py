# Generated by Django 4.0.4 on 2022-06-02 14:26

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_kata_challenge'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_kata',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.kata'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='katas',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, sort_value_field_name='id', to='api.kata'),
        ),
    ]
