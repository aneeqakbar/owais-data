# Generated by Django 4.0 on 2022-01-16 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fetchdata', '0005_outputfileupload_inputfileupload'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('processed_file', models.FileField(upload_to='documents/processed/%Y/%m/%d/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('input_file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='processed_file', to='fetchdata.outputfileupload')),
            ],
        ),
    ]