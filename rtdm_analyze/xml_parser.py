import logging
from typing import Union, Optional
from xml.dom import minidom

from sas_objects import Campaign, Block, DataProcess
from utils import Config
from visualizer import CampaignVisualizer, ProcessVisualizer
from xml_fetcher import SshXmlFetcher

log = logging.getLogger(__name__)


class XmlParser:
    """Парсер XML-файла."""

    AVAILABLE_BLOCK_TYPES = ('SubDiagramNodeDataDO', 'ProcessNodeDataDO')

    def __init__(self,
                 filepath: str,
                 config: Config,
                 subdiagram: bool = False):
        """
        :param filepath: Путь к XML-файлу
        :param config: Конфигурация утилиты
        :param subdiagram: Парсим ли сабдиаграмму
        """
        self.config = config
        self.subdiagram = subdiagram

        self._dom = minidom.parse(filepath)
        self._dom.normalize()

        self._result = {
            'campaigns': [],
            'blocks': [],
            'data_processes': [],
        }
        self._campaign_id = None

    def run(self) -> dict[str, list[Union[Campaign, Block, DataProcess]]]:
        """Запуск парсера."""
        self._parse_campaigns()
        self._parse_blocks()
        self._remove_duplicates()

        # Визуализируем результат только на самом верхнем уровне.
        if not self.subdiagram:
            self._visualize_result()

        return self._result

    def _remove_duplicates(self) -> None:
        """Удали дубликаты."""
        for entity in ('campaigns', 'data_processes',):
            used_ids = set()
            cleaned_entities = []
            for elem in self._result[entity]:
                if elem.id not in used_ids:
                    cleaned_entities.append(elem)
                    used_ids.add(elem.id)
            self._result[entity] = cleaned_entities

    def _parse_campaigns(self) -> None:
        """Спарси кампанию."""
        campaign_nodes = self._dom.getElementsByTagName('CampaignDO')
        if not campaign_nodes:
            log.warning('CampaignDO not found in XML file.')
            return
        campaigns_count = len(campaign_nodes)
        if campaigns_count > 1:
            log.warning(f'Found {campaigns_count} campaigns in XML file, '
                        f'1 was expected.')

        campaign = Campaign(id='', name='')

        # Кампания в XML-файле может быть только одна.
        for node in campaign_nodes[0].childNodes:
            if campaign.id and campaign.name:
                break
            if node.nodeName == 'Id':
                campaign.id = self._campaign_id = node.childNodes[0].nodeValue
                continue
            if node.nodeName == 'Name':
                campaign.name = node.childNodes[0].nodeValue

        self._result['campaigns'].append(campaign)

    def _parse_blocks(self) -> None:
        """Спарси блоки."""
        for block_type in self.AVAILABLE_BLOCK_TYPES:
            block_nodes = self._dom.getElementsByTagName(block_type)
            if not block_nodes:
                log.info(f'No {block_type} found in XML file.')
                continue
            for block_node in block_nodes:
                block = Block(id='',
                              name='',
                              type=block_type,
                              campaign_id=self._campaign_id,
                              data_process_id_list=[])
                for node in block_node.childNodes:
                    if node.nodeName == 'NodeId':
                        block.id = node.childNodes[0].nodeValue
                        continue
                    if node.nodeName == 'NodeName':
                        block.name = node.childNodes[0].nodeValue
                        continue
                    if block_type == 'SubDiagramNodeDataDO':
                        if node.nodeName == 'SubdiagramId':
                            block.subdiagram_id = node.childNodes[0].nodeValue
                            continue
                        if node.nodeName == 'SubdiagramName':
                            block.subdiagram_name = \
                                node.childNodes[0].nodeValue

                if block_type == 'SubDiagramNodeDataDO':
                    block.data_process_id_list.extend(
                        self._parse_subdiagram_block(block.subdiagram_name)
                    )
                else:
                    block.data_process_id_list.append(
                        self._parse_data_process(
                            block_type=block_type,
                            block_node=block_node,
                            block_id=block.id
                        )
                    )
                self._result['blocks'].append(block)

    def _parse_subdiagram_block(self, subdiagram_name: str) -> list[str]:
        """
        Спарси блок сабдиаграмм.
        :param subdiagram_name: Название сабдиаграммы
        :return: Список идентификаторов всех дата-процессов сабдиаграммы
        """
        xml_filepath = SshXmlFetcher(campaign_name=subdiagram_name,
                                     config=self.config).run()
        parsed_xml = XmlParser(xml_filepath, self.config, subdiagram=True)\
            .run()
        for k in self._result.keys():
            self._result[k].extend(parsed_xml.get(k, []))
        return [i.id for i in parsed_xml.get('data_processes', [])]

    def _parse_data_process(self,
                            block_type: str,
                            block_node: minidom.Element,
                            block_id: str) -> Optional[str]:
        """
        Спарси дата-процесс.
        :param block_type: Тип блока
        :param block_node: Нода блока, в которую входит дата-процесс
        :param block_id: Идентификатор блока
        :return: Идентификатор дата-процесса
        """
        # У сабдиаграммы нет дата-процессов.
        if block_type == 'SubDiagramNodeDataDO':
            return

        process_nodes = block_node.getElementsByTagName('Process')
        if not process_nodes:
            log.warning(f'Process not found in {block_type} #{block_id}.')
            return
        process_count = len(process_nodes)
        if process_count > 1:
            log.warning(f'Found {process_count} processes in {block_type} '
                        f'#{block_id}, 1 was expected.')

        data_process = DataProcess(id='',
                                   name='',
                                   lib_name='',
                                   table_name='')

        # Процесс в блоке может быть только один.
        for node in process_nodes[0].childNodes:
            if data_process.id and data_process.name and \
                    data_process.lib_name and data_process.table_name:
                break
            if node.nodeName == 'Id':
                data_process.id = node.childNodes[0].nodeValue
                continue
            if node.nodeName == 'Name':
                data_process.name = node.childNodes[0].nodeValue
                continue
            if node.nodeName == 'LibName':
                data_process.lib_name = node.childNodes[0].nodeValue
                continue
            if node.nodeName == 'TableName':
                data_process.table_name = node.childNodes[0].nodeValue

        self._result['data_processes'].append(data_process)
        return data_process.id

    def _visualize_result(self) -> None:
        """Визуализируй результат."""
        CampaignVisualizer(self._result).run()
        ProcessVisualizer(self._result).run()
