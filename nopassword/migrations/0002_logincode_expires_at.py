import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logincode',
            name='expires_at',
            field=models.DateTimeField(null=True),
        ),
    ]
