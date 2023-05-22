# Generated by Django 4.2.1 on 2023-05-22 14:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("configurator", "0002_remove_image_description_alter_image_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="image",
            name="spec",
        ),
        migrations.AddField(
            model_name="image",
            name="display_name",
            field=models.CharField(
                default="",
                help_text="Human Readable Name of this Image",
                max_length=256,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="image",
            name="tag",
            field=models.CharField(
                default="",
                help_text="Tag of the image to pull from. Eg 2022-01-05, kljhfahlfalksjdf32434. Recommend against using 'latest' tag",
                max_length=1024,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="image",
            name="name",
            field=models.CharField(
                help_text="Name of the image (without the tag). Eg. pangeo/pangeo-notebook, quay.io/your-org/your-image",
                max_length=1024,
            ),
        ),
    ]
