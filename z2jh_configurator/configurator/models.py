from textwrap import dedent
from django.db import models
from django.core.exceptions import ValidationError
import subprocess


class Image(models.Model):
    slug = models.SlugField(
        max_length=256, unique=True,
        help_text="Machine readable name for this image. Autogenerated from display name"
    )
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

    def clean(self):
        """
        Validate that this image actually exists
        """
        # We use skopeo to check if this image exists. This is far more
        # comprehensive than any python based library I have found. It takes
        # a while (a few seconds!) but this is a single tenant application where
        # new images are not added *that* frequently - so this is ok.
        proc = subprocess.run([
            'skopeo',
            '--override-os', 'linux',
            'inspect',
            f'docker://{self.name}:{self.tag}'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if proc.returncode != 0:
            raise ValidationError(f'Docker image {self.name}:{self.tag} not found')


    def __str__(self):
        return f"{self.display_name} <{self.name}:{self.tag}>"


class ProfileImage(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    is_default = models.BooleanField("Default image?")

    def __str__(self):
        return f"{self.image.display_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "image"],
                name="unique_image_per_profile",
                violation_error_message="An image can be present only once in a profile",
            ),
        ]


class Profile(models.Model):
    slug = models.SlugField(
        max_length=256, unique=True,
        help_text="Machine readable name for this image. Autogenerated from display name"
    )
    display_name = models.CharField(max_length=256)
    description = models.TextField()
    images = models.ManyToManyField(Image, through=ProfileImage)
    is_default = models.BooleanField("Default selected profile?")
    nodegroups = models.ManyToManyField("NodeGroup", through="ProfileNodeGroup")

    def to_dict(self):
        """
        Provide a *full* dict representation of this profile
        """
        d = {
            'display_name': self.display_name,
            'slug': self.slug,
            'default': self.is_default,
            'kubespawner_override': {}
        }

        images = self.images.through.objects.all()
        if len(images) > 1:
            d.setdefault('profile_options', {})
            d['profile_options']['image'] = {
                'display_name': 'Image',
                'choices': {}
            }
            for image in images:
                choice = {
                    'display_name': image.image.display_name,
                    'kubespawner_override': {
                        'image': f'{image.image.name}:{image.image.tag}'
                    },
                    'default': image.is_default
                }
                d['profile_options']["choices"]['image'][image.image.slug] = choice # FIXME
        elif len(images) == 1:
            image = images[0]
            d['kubespawner_override']['image'] = f'{image.image.name}:{image.image.tag}'


        nodegroups = self.nodegroups.through.objects.all()

        if len(nodegroups) > 1:
            # We offer a hcoice of nodegroups
            d.setdefault('profile_options', {})
            d['profile_options']['nodegroup'] = {
                'display_name': 'Node Group',
                'choices': {}
            }

            for ng in nodegroups:
                choice = {
                    'display_name': ng.nodegroup.display_name,
                    'kubespawner_override': {
                        'node_selector': ng.nodegroup.node_selector,
                    },
                    'default': ng.is_default
                }
                d['profile_options']['nodegroup']['choices'][ng.nodegroup.slug] = choice
        elif len(nodegroups) == 1:
            d['kubespawner_override']['node_selector'] = nodegroups[0].nodegroup.node_selector

        return d

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_default"],
                condition=models.Q(is_default=True),
                name="only_one_default_profile",
                violation_error_message="Only one profile can be set as default, and a default profile already exists"
            )
        ]

    def __str__(self):
        return self.display_name


class NodeGroup(models.Model):
    slug = models.SlugField(unique=True)
    display_name = models.CharField(max_length=256)
    node_selector = models.JSONField(unique=True)

    def __str__(self):
        return self.display_name


class ProfileNodeGroup(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    nodegroup = models.ForeignKey("NodeGroup", on_delete=models.CASCADE)
    is_default = models.BooleanField()

    def __str__(self):
        return f"{self.nodegroup.display_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "nodegroup"],
                name="unique_nodegroup_per_profile",
                violation_error_message="A nodegroup can be present only once in a profile",
            ),
        ]
