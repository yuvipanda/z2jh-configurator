from django.core.management.base import BaseCommand, CommandError
from ...models import NodeGroup
import json


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("config-file")

    def handle(self, *args, **options):
        file_path = options["config-file"]

        with open(file_path) as f:
            nodegroups = json.load(f)

        for ng in nodegroups:
            existing = NodeGroup.objects.filter(slug=ng["slug"]).first()
            if existing is None:
                existing = NodeGroup(slug=ng["slug"])
                self.stdout.write(f'New NodeGroup {ng["slug"]} found')

            existing.node_selector = ng['node_selector']
            existing.display_name = ng['display_name']
            existing.gpu_count  = ng.get('gpu_count', 0)
            existing.save()
