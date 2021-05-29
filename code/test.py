import logging
import sys

from code.utils import ConfigReader
from code.xml_fetcher import SshXmlFetcher
from code.xml_parser import XmlParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

CONFIG = ConfigReader().config


def test_xml_fetcher():
    ssh_fetcher = SshXmlFetcher(campaign_name='HACK1_MAIN',
                                config=CONFIG)
    print(ssh_fetcher.run())


def test_xml_parser():
    from pprint import pprint
    test_xml = ('/Users/dirtrider/Documents/python_projects/'
                'gpbhack_not_set/code/tmp/campaign_hack1_main.xml')
    pprint(XmlParser(test_xml, CONFIG).run())


if __name__ == '__main__':
    # test_xml_fetcher()
    test_xml_parser()
