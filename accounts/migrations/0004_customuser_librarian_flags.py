from django.db import migrations, models


def mark_existing_librarians(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    # Existing librarians: role librarian OR staff/superuser.
    CustomUser.objects.filter(role="librarian").update(is_librarian=True)
    CustomUser.objects.filter(is_staff=True).update(is_librarian=True)
    CustomUser.objects.filter(is_superuser=True).update(is_librarian=True, is_head_librarian=True)


def unmark_existing_librarians(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    # Reversible (best-effort).
    CustomUser.objects.update(is_librarian=False, is_head_librarian=False)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_migrate_student_to_guest"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_librarian",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="customuser",
            name="is_head_librarian",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(mark_existing_librarians, reverse_code=unmark_existing_librarians),
    ]

