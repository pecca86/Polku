# Generated by Django 3.0.3 on 2020-11-25 08:10

from django.db import migrations, models
import django.db.models.deletion
import django.forms.widgets
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('juttu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Laite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IMEI', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('IMEI2', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('IMEI3', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('sarjanumero', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('sinettipussi_id', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('valmistaja', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('malli', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('kapasiteetti', models.IntegerField(default=0, verbose_name='Koko (GB)')),
                ('kayttojarjestelma', models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='Käyttöjärjestelmä')),
                ('chipset', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('laite_suojakoodi', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('pakkokeinonro', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('esinenro', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('kirjauspvm', models.DateField(default=django.utils.timezone.now, verbose_name=django.forms.widgets.SelectDateWidget)),
                ('lisatietoja', models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='Lisätietoja')),
                ('raporttiin', models.BooleanField(default=True)),
                ('juttu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='juttus', to='juttu.Juttu')),
            ],
        ),
        migrations.CreateModel(
            name='LaiteDataStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laite_data_status', models.CharField(blank=True, max_length=512)),
                ('on_aktiivinen', models.BooleanField(default=True)),
                ('datatyyppi_sailytyksessa', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LaiteSijainti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laitesijainti', models.CharField(blank=True, max_length=512)),
                ('on_aktiivinen', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LaiteStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laite_status', models.CharField(blank=True, max_length=512)),
                ('on_aktiivinen', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LaiteTyyppi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laitetyyppi', models.CharField(blank=True, max_length=512)),
                ('on_aktiivinen', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OheislaiteSijainti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oheislaitesijainti', models.CharField(blank=True, max_length=512)),
                ('on_aktiivinen', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oheislaitetyyppi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oheislaitetyyppi', models.CharField(blank=True, max_length=512)),
                ('on_aktiivinen', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OheisLaite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valmistaja', models.CharField(default='', max_length=512)),
                ('malli', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('sarjanumero', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('oheislaite_suojakoodi', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('ICCID', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('IMSI', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('kapasiteetti', models.IntegerField(default=0, verbose_name='Koko (GB)')),
                ('kirjauspvm', models.DateField(default=django.utils.timezone.now, verbose_name=django.forms.widgets.SelectDateWidget)),
                ('lisatietoja', models.CharField(blank=True, default='', max_length=512, null=True, verbose_name='Lisätietoja')),
                ('raporttiin', models.BooleanField(default=True)),
                ('laite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varsinainen_laite', to='laite.Laite')),
                ('oheislaite_sijainti', models.ForeignKey(limit_choices_to={'on_aktiivinen': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='laite.OheislaiteSijainti')),
                ('oheislaite_status', models.ForeignKey(default='Otettu vastaan', limit_choices_to={'on_aktiivinen': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='laite.LaiteStatus')),
                ('oheislaite_tyyppi', models.ForeignKey(limit_choices_to={'on_aktiivinen': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oheislaite_ohtyyppi', to='laite.Oheislaitetyyppi')),
            ],
        ),
        migrations.CreateModel(
            name='LaiteMuistiinpano',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('laite_muistiinpano', models.TextField(blank=True)),
                ('kirjauspvm', models.DateField(default=django.utils.timezone.now, verbose_name=django.forms.widgets.SelectDateWidget)),
                ('raporttiin', models.BooleanField(default=True)),
                ('parsitut_sovellukset', models.CharField(blank=True, default='', max_length=512)),
                ('parsimatta_jaaneet_sovellukset', models.CharField(blank=True, default='', max_length=512)),
                ('physical', models.BooleanField(default=False)),
                ('fullfilesystem', models.BooleanField(default=False)),
                ('filesystem', models.BooleanField(default=False)),
                ('apk_downgrade', models.BooleanField(default=False)),
                ('logical', models.BooleanField(default=False)),
                ('live', models.BooleanField(default=False)),
                ('laite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laite_note', to='laite.Laite')),
            ],
        ),
        migrations.AddField(
            model_name='laite',
            name='laite_data_status',
            field=models.ForeignKey(blank=True, limit_choices_to={'on_aktiivinen': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='laite.LaiteDataStatus'),
        ),
        migrations.AddField(
            model_name='laite',
            name='laite_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laite_laitestatus', to='laite.LaiteStatus'),
        ),
        migrations.AddField(
            model_name='laite',
            name='laite_tyyppi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laite_laitetyyppi', to='laite.LaiteTyyppi'),
        ),
        migrations.AddField(
            model_name='laite',
            name='sijainti',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='laite_laitesijainti', to='laite.LaiteSijainti'),
        ),
    ]