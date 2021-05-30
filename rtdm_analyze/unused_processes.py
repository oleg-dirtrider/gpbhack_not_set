import logging

from db import DBRunner

log = logging.getLogger(__name__)


class LogsParser:
    """Парсер логов ExportPackage."""

    def __init__(self, filepath: str):
        """
        :param filepath: Путь к файлу с логами
        """
        self.filepath = filepath

    def run(self) -> list[str]:
        """
        Спарси логи.
        :return: Список названий всех дата-процессов
        """
        with open(self.filepath, 'r') as f:
            logs = f.read()
        process_names = [i.strip() for i in logs.split('\n') if
                         i.strip().startswith('/')]
        return [i.split('/')[-1] for i in process_names[1:]]


class UnusedProcessFinder:
    """Поиск неиспользуемых дата-процессов."""

    def __init__(self, export_package_data_filepath: str):
        """
        :param export_package_data_filepath: Путь к файлу с логами
        """
        self.all_packages = LogsParser(export_package_data_filepath).run()
        self.used_packages = DBRunner().get_all_data_processes()

    def run(self) -> list[str]:
        """Найди неиспользуемые дата-процессы."""
        return list(set(self.all_packages) - set(self.used_packages))
