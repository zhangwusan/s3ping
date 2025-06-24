import yaml
import os

class Settings:
    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.load_settings()

    def load_settings(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)

        self.request_engine = config.get('request_engine', {})
        self.middlewares = config.get('middlewares', [])
        self.logging = config.get('logging', {})

    def get_request_engine(self):
        return self.request_engine

    def get_middlewares(self):
        return self.middlewares

    def get_logging_settings(self):
        return self.logging

settings = Settings()