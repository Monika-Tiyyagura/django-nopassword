# nopassword/migrations/0005_logincode_populate_uuid_and_swap_id.py

from django.db import migrations, models
import uuid

def populate_uuids(apps, schema_editor):
    """
    Step 2: Populate UUIDs for all existing LoginCode entries using PostgreSQL's gen_random_uuid()
    Requires the pgcrypto extension to be enabled beforehand.
    """
    schema_editor.execute("""
        UPDATE nopassword_logincode
        SET uuid = gen_random_uuid()
    """)

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0004_logincode_add_uuid_field'),
    ]

    operations = [
        # Step 2: Populate UUIDs
        migrations.RunPython(populate_uuids, reverse_code=migrations.RunPython.noop),

        # Step 3: Remove the old integer 'id' field
        migrations.RemoveField(
            model_name='logincode',
            name='id',
        ),

        # Step 4: Rename the 'uuid' field to 'id'
        migrations.RenameField(
            model_name='logincode',
            old_name='uuid',
            new_name='id',
        ),

        # Step 5: Alter the new 'id' field to be the primary key with default value
        migrations.AlterField(
            model_name='logincode',
            name='id',
            field=models.UUIDField(
                primary_key=True,
                default=uuid.uuid4,
                editable=False,
                serialize=False,
            ),
        ),
    ]
