# Generated by Django 3.2.5 on 2021-07-25 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Required_speciality', models.CharField(max_length=150)),
                ('Date_of_Appointment', models.DateField()),
                ('Start_Time_of_Appointment', models.TextField()),
                ('End_Time_of_Appointment', models.TextField()),
                ('Contect', models.BigIntegerField()),
                ('Doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.doctor')),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
            ],
        ),
    ]
