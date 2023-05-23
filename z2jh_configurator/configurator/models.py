from textwrap import dedent
from django.db import models


class Image(models.Model):
    display_name = models.CharField(
        max_length=256, help_text="Human Readable Name of this Image"
    )
    name = models.CharField(
        max_length=1024,
        help_text=dedent(
            """
        Name of the image (without the tag).

        Eg. pangeo/pangeo-notebook, quay.io/your-org/your-image
        """
        ),
    )
    tag = models.CharField(
        max_length=1024,
        help_text=dedent(
            """
        Tag of the image to pull from.

        Eg 2022-01-05, kljhfahlfalksjdf32434. Recommend against using 'latest' tag"""
        ),
    )

    def __str__(self):
        return f"{self.display_name} <{self.name}:{self.tag}>"



class ProfileImage(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_default = models.BooleanField("Default image?")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'image'], name='unique_image_per_profile', violation_error_message="An image can be present only once in a profile"),
        ]
                                

class Profile(models.Model):
    display_name = models.CharField(max_length=256)
    description = models.TextField()
    image = models.ManyToManyField(Image, through=ProfileImage)

    def __str__(self):
        return self.display_name

