# Generated by Django 3.2.25 on 2024-07-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='name',
            field=models.CharField(default='fsd', max_length=100),
            preserve_default=False,
        ),
    ]