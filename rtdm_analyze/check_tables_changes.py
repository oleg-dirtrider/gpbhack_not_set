import argparse
import logging
import sys

from db import DBRunner
from utils import ConfigReader
from xml_fetcher import SshXmlFetcher, XmlFetcher
from xml_parser import XmlParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('campaign_name', type=str)
    parser.add_argument("-l", "--local", dest="local", action="store_true")
    args = parser.parse_args()

    config = ConfigReader().config
    xml_fetcher = XmlFetcher(args.campaign_name, config) if \
        args.local else SshXmlFetcher(args.campaign_name, config)
    xml_file_path = xml_fetcher.run()
    xml_parser = XmlParser(xml_file_path, config, local=args.local)
    data_processes = xml_parser.run().get('data_processes')

    from pprint import pprint
    pprint(DBRunner().check(data_processes))
