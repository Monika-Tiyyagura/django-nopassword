from django.db import migrations
import uuid

def populate_uuids(apps, schema_editor):
    Logincode = apps.get_model('nopassword', 'logincode')
    db_alias = schema_editor.connection.alias

    for obj in Logincode.objects.using(db_alias).all():
        Logincode.objects.using(db_alias).filter(pk=obj.pk).update(uuid=uuid.uuid4())

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
            field=migrations.fields.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
        ),
    ]
