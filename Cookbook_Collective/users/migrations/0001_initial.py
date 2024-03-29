# Generated by Django 4.2.9 on 2024-01-29 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120)),
                ('saved_recipes', models.ManyToManyField(blank=True, related_name='saved_by_users', to='recipes.recipe')),
            ],
        ),
    ]
