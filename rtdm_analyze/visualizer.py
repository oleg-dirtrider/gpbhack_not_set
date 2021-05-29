import logging
import os
import sys
from collections import defaultdict
from typing import Union

from graphviz import Digraph

from sas_objects import Campaign, Block, DataProcess

log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class CampaignVisualizer:
    """Визуализация связей Кампании -> Процессы."""

    VIS_FOLDER = os.path.join(
        os.path.dirname(__file__), 'visualized_results', 'campaigns'
    )
    MAIN_RENDER_FILENAME = 'all_campaigns.gv'

    def __init__(
            self,
            parsed_xml: dict[str, list[Union[Campaign, Block, DataProcess]]]
    ):
        """
        :param parsed_xml: Результаты парсера XML из SAS
        """
        self.parsed_xml = parsed_xml
        self.dot = Digraph(comment='RTDM analysis')

        self._edges = defaultdict(list)

    def run(self) -> None:
        """Запусти визуализатор."""
        self._set_nodes()
        self._set_edges()
        self.dot.render(os.path.join(
            self.VIS_FOLDER, self.MAIN_RENDER_FILENAME
        ))
        log.info(f'Graph "{self.MAIN_RENDER_FILENAME}" visualized.')
        self._get_individual_graphs()

    def _set_nodes(self) -> None:
        """Установи вершины графа."""
        entities_titles_map = {
            'campaigns': 'Campaign',
            'data_processes': 'DataProcess',
        }
        counter = 0
        for k, v in entities_titles_map.items():
            for entity in self.parsed_xml.get(k, []):
                entity.vis_id = str(counter)
                self.dot.node(entity.vis_id, f'{v} "{entity.name}"')
                counter += 1

    def _set_edges(self) -> None:
        """Установи ребра графа."""
        campaigns = {
            i.id: i for i in self.parsed_xml.get('campaigns', [])
        }
        processes = {
            i.id: i for i in self.parsed_xml.get('data_processes', [])
        }
        graph_edges = []
        for block in self.parsed_xml.get('blocks', []):
            campaign = campaigns.get(block.campaign_id)
            if not campaign:
                log.warning(f'Campaign not found for block #{block.id}!')
                continue
            for process_id in block.data_process_id_list:
                process = processes.get(process_id)
                if process:
                    if self.__class__.__name__ == 'CampaignVisualizer':
                        edge = (campaign.vis_id, process.vis_id,)
                        if edge not in set(graph_edges):
                            graph_edges.append(edge)
                            self._edges[campaign.id].append(edge)
                    else:
                        edge = (process.vis_id, campaign.vis_id,)
                        if edge not in set(graph_edges):
                            graph_edges.append(edge)
                            self._edges[process.id].append(edge)
        self.dot.edges(graph_edges)

    def _get_individual_graphs(self) -> None:
        """Получи отдельные графы для каждой кампании."""
        for campaign in self.parsed_xml.get('campaigns', []):
            dot = Digraph(comment=f'{campaign.name} analysis')
            dot.node(campaign.vis_id, f'Campaign "{campaign.name}"')

            campaign_edges = self._edges[campaign.id]
            process_vis_ids = [i[1] for i in campaign_edges]
            for process in self.parsed_xml.get('data_processes', []):
                if process.vis_id in set(process_vis_ids):
                    dot.node(process.vis_id, f'DataProcess "{process.name}"')

            dot.edges(campaign_edges)
            graph_name = f'campaign_{campaign.name}.gv'
            dot.render(os.path.join(self.VIS_FOLDER, graph_name))
            log.info(f'Graph "{graph_name}" visualized.')


class ProcessVisualizer(CampaignVisualizer):
    """Визуализация связей Процессы -> Кампании."""

    VIS_FOLDER = os.path.join(
        os.path.dirname(__file__), 'visualized_results', 'data_processes'
    )
    MAIN_RENDER_FILENAME = 'all_data_processes.gv'

    def _get_individual_graphs(self) -> None:
        """Получи отдельные графы для каждого дата-процесса."""
        for process in self.parsed_xml.get('data_processes', []):
            dot = Digraph(comment=f'{process.name} analysis')
            dot.node(process.vis_id, f'DataProcess "{process.name}"')

            process_edges = self._edges[process.id]
            campaign_vis_ids = [i[1] for i in process_edges]
            for campaign in self.parsed_xml.get('campaigns', []):
                if campaign.vis_id in set(campaign_vis_ids):
                    dot.node(campaign.vis_id, f'Campaign "{campaign.name}"')

            dot.edges(process_edges)
            graph_name = f'data_process_{process.name}.gv'
            dot.render(os.path.join(self.VIS_FOLDER, graph_name))
            log.info(f'Graph "{graph_name}" visualized.')
