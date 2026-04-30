from django.db import migrations


def migrate_student_to_guest(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    CustomUser.objects.filter(role="student").update(role="guest")


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_customuser_profile_pic_alter_customuser_role"),
    ]

    operations = [
        migrations.RunPython(migrate_student_to_guest, migrations.RunPython.noop),
    ]

