import logging
import sys

from rtdm_analyze.visualizer import CampaignVisualizer, ProcessVisualizer
from sas_objects import Block, Campaign, DataProcess
from utils import ConfigReader
from xml_fetcher import SshXmlFetcher
from xml_parser import XmlParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

CONFIG = ConfigReader().config


def test_xml_fetcher():
    ssh_fetcher = SshXmlFetcher(campaign_name='HACK1_MAIN',
                                config=CONFIG)
    print(ssh_fetcher.run())


def test_xml_parser():
    from pprint import pprint
    test_xml = ('/Users/dirtrider/Documents/python_projects/'
                'gpbhack_not_set/rtdm_analyze/tmp/campaign_hack1_main.xml')
    pprint(XmlParser(test_xml, CONFIG).run())


def test_visualize():
    test_data = {'blocks': [
        Block(id='HBCCBQG3UBE3TP02', name='READ_DOC', type='ProcessNodeDataDO',
              campaign_id='DGFDZTZFNBHPVLG2',
              data_process_id_list=['CHHBBPOBK3EBT45Y'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='GBDH1YVIKJFIU42C', name='READ_ADDRESS',
              type='ProcessNodeDataDO', campaign_id='DGFDZTZFNBHPVLG2',
              data_process_id_list=['AFBGVE032NBWXACF'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='FFDACGCBZJDQSZFZ', name='INCOME', type='ProcessNodeDataDO',
              campaign_id='DGFDZTZFNBHPVLG2',
              data_process_id_list=['BDDAORJDAFGOUFMB'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='EADCLERNRNHQTPES', name='RESULT_CHECKS',
              type='SubDiagramNodeDataDO', campaign_id='CBFBJ0YIVFBKXPIT',
              data_process_id_list=['CHHBBPOBK3EBT45Y', 'AFBGVE032NBWXACF',
                                    'BDDAORJDAFGOUFMB'],
              subdiagram_id='BBEEK5UJFVGRTPER',
              subdiagram_name='HACK1_RESULT_CHECKS'),
        Block(id='DCBG0CHZURBXVLIL', name='ADDR_CHECK',
              type='ProcessNodeDataDO', campaign_id='HAGG1UVFYBDKUPL3',
              data_process_id_list=['CHFGITJOYFEXX2HV'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='DCCFUX0C1JEUSGWJ', name='READ_DOCS',
              type='ProcessNodeDataDO', campaign_id='HAGG1UVFYBDKUPL3',
              data_process_id_list=['BGFBGCTH2RHRS5LK'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='BFGDF4B2UREWQESY', name='READ_ADDRESS',
              type='ProcessNodeDataDO', campaign_id='HAGG1UVFYBDKUPL3',
              data_process_id_list=['DFGDGEMU5NESWYKK'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='GDBF4W4ZNRCNTHUI', name='GET_CLIENT',
              type='ProcessNodeDataDO', campaign_id='HAGG1UVFYBDKUPL3',
              data_process_id_list=['HGBAVM2TNVETWF35'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='FHFGYO2MAZD3RLMF', name='ADDR_DOC_CHECK',
              type='ProcessNodeDataDO', campaign_id='HAGG1UVFYBDKUPL3',
              data_process_id_list=['CHFGITJOYFEXX2HV'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='AFFA2HV4NBHTQOKA', name='ADDRESS_CHECKS',
              type='SubDiagramNodeDataDO', campaign_id='EDGCGY5NHFDPRCLV',
              data_process_id_list=['CHFGITJOYFEXX2HV', 'BGFBGCTH2RHRS5LK',
                                    'DFGDGEMU5NESWYKK', 'HGBAVM2TNVETWF35'],
              subdiagram_id='ACBF0RNFF3DVSGA2',
              subdiagram_name='HACK1_ADDRESS_CHECKS'),
        Block(id='AGHHYR2OVNERWHAK', name='READ_CLIENT',
              type='ProcessNodeDataDO', campaign_id='CGAE43ALKBEQVDMS',
              data_process_id_list=['HGBAVM2TNVETWF35'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='AFEHM32CUZDVTHEX', name='INS_CHECK',
              type='ProcessNodeDataDO', campaign_id='CGAE43ALKBEQVDMS',
              data_process_id_list=['CHFGITJOYFEXX2HV'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='ECBGYH21AVCLT1JF', name='READ_DOC', type='ProcessNodeDataDO',
              campaign_id='CGAE43ALKBEQVDMS',
              data_process_id_list=['GDGAOTNOIFDTQPRI'], subdiagram_id=None,
              subdiagram_name=None),
        Block(id='HEEAWCU45FFSWU4A', name='DOC_CHECKS',
              type='SubDiagramNodeDataDO', campaign_id='EDGCGY5NHFDPRCLV',
              data_process_id_list=['HGBAVM2TNVETWF35', 'CHFGITJOYFEXX2HV',
                                    'GDGAOTNOIFDTQPRI'],
              subdiagram_id='DDAAX4WIAVC5RTNI',
              subdiagram_name='HACK1_DOC_CHECKS'),
        Block(id='BBAECGQZSJAIXZTL', name='CLIENT_CHECKS',
              type='SubDiagramNodeDataDO', campaign_id='CBFBJ0YIVFBKXPIT',
              data_process_id_list=['CHFGITJOYFEXX2HV', 'BGFBGCTH2RHRS5LK',
                                    'DFGDGEMU5NESWYKK', 'HGBAVM2TNVETWF35',
                                    'GDGAOTNOIFDTQPRI'],
              subdiagram_id='DADFNM5CZNEXW0HQ',
              subdiagram_name='HACK1_CLIENT_CHECKS'),
        Block(id='HECG1MAA03G5SPP2', name='GET_CLIENT',
              type='ProcessNodeDataDO', campaign_id='CBFBJ0YIVFBKXPIT',
              data_process_id_list=['DDABXSDC13B1TJX3'], subdiagram_id=None,
              subdiagram_name=None)],
                   'campaigns': [
                       Campaign(id='CBFBJ0YIVFBKXPIT', name='HACK1_MAIN'),
                       Campaign(id='DGFDZTZFNBHPVLG2',
                                name='HACK1_RESULT_CHECKS'),
                       Campaign(id='EDGCGY5NHFDPRCLV',
                                name='HACK1_CLIENT_CHECKS'),
                       Campaign(id='HAGG1UVFYBDKUPL3',
                                name='HACK1_ADDRESS_CHECKS'),
                       Campaign(id='CGAE43ALKBEQVDMS',
                                name='HACK1_DOC_CHECKS')],
                   'data_processes': [DataProcess(id='CHHBBPOBK3EBT45Y',
                                                  name='READ_DOCUMENT_v2',
                                                  lib_name='HACK1_INT',
                                                  table_name='DOCUMENT'),
                                      DataProcess(id='AFBGVE032NBWXACF',
                                                  name='READ_ADDRESS_v2',
                                                  lib_name='HACK1_INT',
                                                  table_name='ADDRESS'),
                                      DataProcess(id='BDDAORJDAFGOUFMB',
                                                  name='READ_INCOME',
                                                  lib_name='HACK1_INT',
                                                  table_name='INCOME'),
                                      DataProcess(id='CHFGITJOYFEXX2HV',
                                                  name='INS_CHECK',
                                                  lib_name='HACK1_MAIN',
                                                  table_name='CHECKS'),
                                      DataProcess(id='BGFBGCTH2RHRS5LK',
                                                  name='READ_DOCUMENT_v1',
                                                  lib_name='HACK1_INT',
                                                  table_name='DOCUMENT'),
                                      DataProcess(id='DFGDGEMU5NESWYKK',
                                                  name='READ_ADDRESS',
                                                  lib_name='HACK1_INT',
                                                  table_name='ADDRESS'),
                                      DataProcess(id='HGBAVM2TNVETWF35',
                                                  name='CLIENT_v2',
                                                  lib_name='HACK1_INT',
                                                  table_name='CLIENT'),
                                      DataProcess(id='GDGAOTNOIFDTQPRI',
                                                  name='READ_DOCUMENT',
                                                  lib_name='HACK1_INT',
                                                  table_name='DOCUMENT'),
                                      DataProcess(id='DDABXSDC13B1TJX3',
                                                  name='CLIENT',
                                                  lib_name='HACK1_INT',
                                                  table_name='CLIENT')]}

    CampaignVisualizer(test_data).run()
    ProcessVisualizer(test_data).run()


if __name__ == '__main__':
    # test_xml_fetcher()
    test_xml_parser()
    # test_visualize()
