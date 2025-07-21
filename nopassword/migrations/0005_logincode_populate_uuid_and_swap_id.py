#0005_logincode_populate_uuid_and_swap_id.py

from django.db import migrations, models
import uuid

def populate_uuids(apps, schema_editor):
    LoginCode = apps.get_model('nopassword', 'LoginCode')
    for code in LoginCode.objects.all():
        code.uuid = uuid.uuid4()
        code.save(update_fields=["uuid"])

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0004_logincode_add_uuid_field'),
    ]

    operations = [
        # Step 2: Populate UUIDs
        migrations.RunPython(populate_uuids, reverse_code=migrations.RunPython.noop),

        # Step 3: Remove old ID field
        migrations.RemoveField(
            model_name='logincode',
            name='id',
        ),

        # Step 4: Rename 'uuid' to 'id'
        migrations.RenameField(
            model_name='logincode',
            old_name='uuid',
            new_name='id',
        ),

        # Step 5: Alter the new 'id' to be primary key with default
        migrations.AlterField(
            model_name='logincode',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
        ),
    ]
