from .resource_path import resource_path
import yaml

def read_config():
    with open(resource_path("config/config.yaml"), "r") as file:
        return yaml.safe_load(file)