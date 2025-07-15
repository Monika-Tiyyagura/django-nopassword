# 0005_logincode_populate_uuid_and_swap_id.py
from django.db import migrations, models
import uuid

def populate_uuids(apps, schema_editor):
    cursor = schema_editor.connection.cursor()
    cursor.execute('SELECT id FROM nopassword_logincode')
    rows = cursor.fetchall()

    for row in rows:
        int_id = row[0]
        new_uuid = str(uuid.uuid4())
        cursor.execute(
            'UPDATE nopassword_logincode SET uuid = %s WHERE id = %s',
            [new_uuid, int_id]
        )

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0004_logincode_add_uuid_field'),
    ]

    operations = [
        migrations.RunPython(populate_uuids, reverse_code=migrations.RunPython.noop),
        
        # Step 2: Remove the old PK
        migrations.RemoveField(
            model_name='logincode',
            name='id',
        ),
        # Step 3: Rename `uuid` to `id`
        migrations.RenameField(
            model_name='logincode',
            old_name='uuid',
            new_name='id',
        ),
        # Step 4: Make `id` the new PK
        migrations.AlterField(
            model_name='logincode',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
        ),
    ]
