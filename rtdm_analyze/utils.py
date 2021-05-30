import logging
import os
import time
from typing import NamedTuple, Any, Optional

import paramiko
import yaml

log = logging.getLogger(__name__)

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
            **self.read_yaml_config(filepath=CONFIG_FILEPATH),
            sas_password=os.getenv('SAS_PASSWORD'),
            ssh_sas_password=os.getenv('SSH_SAS_PASSWORD')
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


class SshConnector:
    """Коннектор к удаленному серверу по SSH."""

    def __init__(self, config: Config):
        """
        :param config: Конфигурация утилиты
        """
        if not (config.ssh_sas_host and config.ssh_sas_port and
                config.ssh_sas_user and config.ssh_sas_password):
            raise Exception('Not all SSH connection parameters are filled '
                            'in the configuration file.')
        self.config = config
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self) -> None:
        """Подключись к серверу."""
        self._client.connect(hostname=self.config.ssh_sas_host,
                             port=self.config.ssh_sas_port,
                             username=self.config.ssh_sas_user,
                             password=self.config.ssh_sas_password)

    def close_conn(self) -> None:
        """Закрой SSH-соединение."""
        self._client.close()

    def send_file(self, localpath: str, remotepath: str) -> None:
        """
        Отправь файл на удаленный сервер.
        :param localpath: Локальный путь к файлу
        :param remotepath: Удаленный путь к файлу
        """
        sftp = self._client.open_sftp()
        sftp.put(localpath, remotepath)
        log.info(f'{localpath} >>> {remotepath}')
        sftp.close()

    def get_file(self, remotepath: str, localpath: str) -> None:
        """
        Получи файл с удаленного сервера.
        :param remotepath: Удаленный путь к файлу
        :param localpath: Локальный путь к файлу
        """
        sftp = self._client.open_sftp()
        sftp.get(remotepath, localpath)
        log.info(f'{remotepath} >>> {localpath}')
        sftp.close()

    def run_command(self, command: str, sleeptime: int = 0.1) -> int:
        """
        Запусти команду на удаленном сервере.
        :param command: Команда
        :param sleeptime: Интервал проверки выполнения команды
        :return: Статус завершения
        """
        session = self._client.get_transport().open_session()
        log.info(f'Running command "{command}".')
        session.exec_command(command)
        while True:
            if session.exit_status_ready():
                break
            time.sleep(sleeptime)
        ext_code = session.recv_exit_status()
        log.info(f'Command finished with code {ext_code}.')
        return ext_code
