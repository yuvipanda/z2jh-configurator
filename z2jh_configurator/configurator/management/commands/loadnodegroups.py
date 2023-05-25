import json
from jsonschema import validate

from django.core.management.base import BaseCommand, CommandError

from ...models import NodeGroup

SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "slug": {
                    "type": "string",
                    "description": "Machine readable, unchangeable slug for this NodeGroup. Allowed characters are a-z,0-9 and -",
                },
                "display_name": {
                    "type": "string",
                    "description": "Human readable name for this NodeGroup",
                },
                "node_selector": {
                    "type": "object",
                    "additional_properties": True,
                    "description": "Kuberentes Node Selector applied when users select this NodeGroup",
                },
            },
            "required": ["slug", "display_name", "node_selector"],
        }
    ],
}


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("config-file")

    def handle(self, *args, **options):
        file_path = options["config-file"]

        with open(file_path) as f:
            nodegroups = json.load(f)

        validate(instance=nodegroups, schema=SCHEMA)

        for ng in nodegroups:
            existing = NodeGroup.objects.filter(slug=ng["slug"]).first()
            if existing is None:
                existing = NodeGroup(slug=ng["slug"])
                self.stdout.write(f'New NodeGroup {ng["slug"]} found')

            existing.node_selector = ng["node_selector"]
            existing.display_name = ng["display_name"]
            existing.gpu_count = ng.get("gpu_count", 0)
            existing.save()
