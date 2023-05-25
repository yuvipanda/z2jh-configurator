from django.apps import AppConfig
from asgiref.sync import sync_to_async
import json


class ConfiguratorConfig(AppConfig):
    name = "z2jh_configurator.configurator"

