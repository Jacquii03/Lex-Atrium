# Generated by Django 3.2.8 on 2021-12-03 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userManagement', '0001_initial'),
        ('caseManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userManagement.user'),
        ),
    ]
