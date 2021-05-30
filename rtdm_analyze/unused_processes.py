import logging

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
