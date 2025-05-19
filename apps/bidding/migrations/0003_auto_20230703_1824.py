

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0002_auto_20230529_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='biddingitem',
            name='observation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='biddingitem',
            name='result',
            field=models.CharField(choices=[('gain', 'Ganho'), ('lost', 'Perdido'), ('pending', 'Pendente')], default='pending', max_length=10),
        ),
    ]
