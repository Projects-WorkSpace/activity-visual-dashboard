# Generated by Django 4.1.5 on 2023-01-16 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0007_delete_activities_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Activities",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
            ],
            options={
                "verbose_name": "Activities",
                "verbose_name_plural": "Activities",
            },
        ),
        migrations.CreateModel(
            name="ChildActivity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                (
                    "activityID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application.activities",
                    ),
                ),
            ],
            options={
                "verbose_name": "Child Activities",
                "verbose_name_plural": "Child Activities",
            },
        ),
        migrations.CreateModel(
            name="UserChild",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("dateOfBirth", models.DateField()),
                (
                    "userID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Children",
                "verbose_name_plural": "User Children",
            },
        ),
        migrations.CreateModel(
            name="ChildDayAcitivity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("points", models.IntegerField(default=0)),
                ("hrs", models.IntegerField(default=0)),
                ("mins", models.IntegerField(default=0)),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "childActivityID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application.childactivity",
                    ),
                ),
            ],
            options={
                "verbose_name": "Child Day Activities",
                "verbose_name_plural": "Child Day Activities",
            },
        ),
        migrations.AddField(
            model_name="childactivity",
            name="childID",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="application.userchild"
            ),
        ),
    ]
