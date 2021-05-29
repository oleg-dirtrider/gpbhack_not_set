import logging
import os
import subprocess
import time

import paramiko

from utils import Config

log = logging.getLogger(__name__)


class XmlFetcher:
    """Получение XML-файла из SAS."""

    TMP_FOLDER = os.path.join(os.path.dirname(__file__), 'tmp')
    SAS_SASMAEXTRACT_PATH = ('/opt/sas/sashome/SASMarketingAutomation'
                             'IntegrationUtilities/6.6/sasmaextract')

    def __init__(self, campaign_name: str, config: Config):
        """
        :param campaign_name: Название кампании для которой получаем XML
        :param config: Конфигурация утилиты
        """
        self.campaign_name = campaign_name
        self.config = config

    def _generate_request_xml(self) -> str:
        """
        Создай xml-файл с запросом к SAS.
        :return: Путь к созданному файлу
        """
        filepath = os.path.join(self.TMP_FOLDER,
                                f'request_{self.campaign_name.lower()}.xml')
        with open(filepath, 'w') as f:
            f.write(f'<MAExtractRequest><CampaignDO detail="ALL">'
                    f'<Name operator="=">{self.campaign_name}</Name>'
                    f'<CampaignType operator="=">decisionCampaign'
                    f'</CampaignType></CampaignDO></MAExtractRequest>')
        return filepath

    def run(self) -> str:
        """
        Запусти получение XML-файла.
        :return: Путь к полученному XML-файлу
        """
        request_filepath = self._generate_request_xml()
        output_filepath = os.path.join(
            self.TMP_FOLDER,
            f'campaign_{self.campaign_name.lower()}.xml'
        )
        command = self._generate_sas_command(request_filepath, output_filepath)
        result = subprocess.run(command, shell=True, capture_output=True)
        if result.returncode == 0:
            return output_filepath
        raise Exception(f'Failed to get XML from SAS. '
                        f'STDOUT: {result.stdout} '
                        f'STDERR: {result.stderr}')

    def _generate_sas_command(self,
                              request_filepath: str,
                              output_filepath: str) -> str:
        """
        Сгенерируй команду на выгрузку XML из SAS.
        :param request_filepath: Путь к XML с конфигурацией запроса
        :param output_filepath: Путь к XML с результатами запроса
        """
        return (f'{self.SAS_SASMAEXTRACT_PATH} {self.config.sas_user} '
                f'{self.config.sas_password} {self.config.sas_auth_type} '
                f'"{self.config.sas_ci_business_space}" {request_filepath} '
                f'{output_filepath}')


class SshXmlFetcher(XmlFetcher):
    """Получение XML-файла из SAS через SSH."""

    def __init__(self, campaign_name: str, config: Config):
        """
        :param campaign_name: Название кампании для которой получаем XML
        :param config: Конфигурация утилиты
        """
        if not (config.ssh_sas_host and config.ssh_sas_port and
                config.ssh_sas_user and config.ssh_sas_password):
            raise Exception('Not all SSH connection parameters are filled '
                            'in the configuration file.')
        super().__init__(campaign_name, config)
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property
    def _ssh_home(self) -> str:
        """Домашняя директория на удаленном сервере."""
        return f'/home/{self.config.ssh_sas_user}/'

    def _connect(self) -> None:
        """Подключись к серверу."""
        self._client.connect(hostname=self.config.ssh_sas_host,
                             port=self.config.ssh_sas_port,
                             username=self.config.ssh_sas_user,
                             password=self.config.ssh_sas_password)

    def _close_conn(self) -> None:
        """Закрой SSH-соединение."""
        self._client.close()

    def run(self) -> str:
        """
        Запусти получение XML-файла.
        :return: Путь к полученному XML-файлу
        """
        self._connect()

        request_filepath = self._generate_request_xml()
        output_filename = f'campaign_{self.campaign_name.lower()}.xml'
        output_filepath = os.path.join(self.TMP_FOLDER, output_filename)

        ssh_request_filepath = (f'{self._ssh_home}'
                                f'{os.path.basename(request_filepath)}')
        ssh_output_filepath = f'{self._ssh_home}{output_filename}'

        # Отправляем XML с конфигурацией запроса на сервер.
        self._send_file(request_filepath, ssh_request_filepath)

        # Получаем с севера XML с результатом запроса.
        command = self._generate_sas_command(ssh_request_filepath,
                                             ssh_output_filepath)
        result_code = self._run_command(command)
        if result_code != 0:
            raise Exception(f'Sasmaextract failed with code {result_code}.')
        self._get_file(ssh_output_filepath, output_filepath)

        self._close_conn()

        if os.path.isfile(output_filepath):
            return output_filepath
        raise Exception('Failed to get XML data from remote server.')

    def _send_file(self, localpath: str, remotepath: str) -> None:
        """
        Отправь файл на удаленный сервер.
        :param localpath: Локальный путь к файлу
        :param remotepath: Удаленный путь к файлу
        """
        sftp = self._client.open_sftp()
        sftp.put(localpath, remotepath)
        log.info(f'{localpath} >>> {remotepath}')
        sftp.close()

    def _get_file(self, remotepath: str, localpath: str) -> None:
        """
        Получи файл с удаленного сервера.
        :param remotepath: Удаленный путь к файлу
        :param localpath: Локальный путь к файлу
        """
        sftp = self._client.open_sftp()
        sftp.get(remotepath, localpath)
        log.info(f'{remotepath} >>> {localpath}')
        sftp.close()

    def _run_command(self, command: str, sleeptime: int = 0.1) -> int:
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
