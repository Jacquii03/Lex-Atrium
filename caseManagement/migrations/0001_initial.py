# Generated by Django 3.2.8 on 2021-12-03 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('case_type', models.CharField(choices=[('criminal', 'criminal'), ('civil', 'civil')], max_length=100)),
                ('status', models.CharField(choices=[('not assigned', 'not assigned'), ('ongoing', 'ongoing'), ('archived', 'archived')], default='not assigned', max_length=150)),
                ('judge_assigned', models.CharField(default='Not assigned', max_length=150)),
                ('judge_assigned_id', models.IntegerField(blank=True, null=True)),
                ('court_assigned', models.CharField(default='Not assigned', max_length=200)),
                ('judgement', models.FileField(blank=True, null=True, upload_to='judgement/')),
            ],
        ),
        migrations.CreateModel(
            name='CaseFolders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_file', models.FileField(upload_to='Case Files/')),
                ('case_file_name', models.CharField(max_length=600)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='caseManagement.case')),
            ],
        ),
    ]
