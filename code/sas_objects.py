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
    campaign_id: str


@dataclass
class DataProcess:
    id: str
    name: str
    block_id: str
    subdiagram_id: str
    lib_name: str
    table_name: str
