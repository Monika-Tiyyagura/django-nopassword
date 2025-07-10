from django.db import migrations, models
import uuid

def convert_integer_id_to_uuid(apps, schema_editor):
    Logincode = apps.get_model('nopassword', 'logincode')
    
    for obj in Logincode.objects.all():
        obj.id = uuid.uuid4()
        obj.save(update_fields=['id'])
        

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0003_alter_logincode_expires_at'),
    ]

    operations = [
        migrations.RunPython(convert_integer_id_to_uuid, reverse_code=migrations.RunPython.noop),

        migrations.AlterField(
            model_name='logincode',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True),
        ),
    ]
