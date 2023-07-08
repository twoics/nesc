# Generated by Django 4.2.3 on 2023-07-08 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0003_reporter_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serves_hot_dogs', models.BooleanField(default=False)),
                ('serves_pizza', models.BooleanField(default=False)),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='test.place')),
            ],
        ),
    ]
