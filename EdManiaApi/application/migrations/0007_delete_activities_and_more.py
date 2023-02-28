# Generated by Django 4.1.5 on 2023-01-16 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0006_userchild_dateofbirth"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Activities",
        ),
        migrations.RemoveField(
            model_name="userchildactivity",
            name="userChildId",
        ),
        migrations.RemoveField(
            model_name="userchilddailyactivity",
            name="childActivityId",
        ),
        migrations.DeleteModel(
            name="UserChild",
        ),
        migrations.DeleteModel(
            name="UserChildActivity",
        ),
        migrations.DeleteModel(
            name="UserChildDailyActivity",
        ),
    ]