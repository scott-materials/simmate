# Generated by Django 3.1.5 on 2021-10-22 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diffusion', '0016_empcorbarrier'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostLattice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dimension', models.IntegerField(blank=True, null=True)),
                ('structure', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='diffusion.materialsprojectstructure')),
            ],
        ),
    ]