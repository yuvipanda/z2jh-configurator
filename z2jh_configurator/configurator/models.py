from django.db import models

class Image(models.Model):
    display_name = models.CharField(max_length=256, help_text="Human Readable Name of this Image")
    name = models.CharField(max_length=1024, help_text="Name of the image (without the tag). Eg. pangeo/pangeo-notebook, quay.io/your-org/your-image")
    tag = models.CharField(max_length=1024, help_text="Tag of the image to pull from. Eg 2022-01-05, kljhfahlfalksjdf32434. Recommend against using 'latest' tag")

    def __str__(self):
        return f"{self.display_name} <{self.name}:{self.tag}>"
    

class Profile(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    

