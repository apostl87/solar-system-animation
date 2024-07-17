from .absolute_path import absolute_path
import yaml

def read_config():
    with open(absolute_path("config/config.yaml"), "r") as file:
        return yaml.safe_load(file)