# Generated by Django 4.1.13 on 2023-12-14 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import site1.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('site1', '0004_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('str', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserQuiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_easy', djongo.models.fields.ArrayField(model_container=site1.models.QuizAttempt)),
                ('quiz_medium', djongo.models.fields.ArrayField(model_container=site1.models.QuizAttempt)),
                ('quiz_hard', djongo.models.fields.ArrayField(model_container=site1.models.QuizAttempt)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
