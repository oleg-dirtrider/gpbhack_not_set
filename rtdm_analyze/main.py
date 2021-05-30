import argparse
import logging
import os
import sys

from db import DBRunner
from utils import ConfigReader
from xml_fetcher import SshXmlFetcher
from xml_parser import XmlParser

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

# для windows
os.environ["PATH"] += os.pathsep + 'С:/Program Files/Graphviz/bin/'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("campaign_name")
    args = parser.parse_args()
    config = ConfigReader().config
    xml_fetcher = SshXmlFetcher(args.campaign_name, config)
    xml_file_path = xml_fetcher.run()
    xml_parser = XmlParser(xml_file_path, config)
    data_for_db = xml_parser.run()
    db_runner = DBRunner()
    db_runner.clear_tables()
    db_runner.insert_data(data=data_for_db)
    print("Вроде сработало!)")

