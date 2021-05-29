import os
from typing import NamedTuple, Any, Optional

import yaml

CONFIG_FILENAME = 'config.yaml'
CONFIG_FILEPATH = os.path.join(os.path.dirname(__file__), CONFIG_FILENAME)


class Config(NamedTuple):
    sas_user: str
    sas_password: str
    sas_auth_type: str
    sas_ci_business_space: str
    ssh_sas_host: Optional[str] = None
    ssh_sas_port: Optional[int] = None
    ssh_sas_user: Optional[str] = None
    ssh_sas_password: Optional[str] = None


class ConfigReader:
    """Получение конфигурации."""

    def __init__(self) -> None:
        self.config = Config(
            **self.read_yaml_config(filepath=CONFIG_FILEPATH)
        )

    @staticmethod
    def read_yaml_config(filepath: str) -> dict[str, Any]:
        """
        Прочитай yml-файл конфигурации.
        :param filepath: Путь к файлу конфигурации
        """
        if not os.path.basename(filepath).endswith(('yml', 'yaml',)):
            raise TypeError('Invalid config file type. '
                            'Only ".yml" or ".yaml" supported.')
        with open(filepath) as file:
            return yaml.safe_load(file)
