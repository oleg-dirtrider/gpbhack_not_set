from dataclasses import dataclass


@dataclass
class Campaign:
    id: str
    name: str


@dataclass
class Block:
    id: str
    name: str
    type: str
    subdiagram_id: str
    campaign_id: str
    data_process_id: str



@dataclass
class DataProcess:
    id: str
    name: str
    lib_name: str
    table_name: str
