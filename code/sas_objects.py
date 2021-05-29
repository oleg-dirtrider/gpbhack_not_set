from dataclasses import dataclass
from typing import Optional


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
    data_process_id: Optional[str] = None
    subdiagram_id: Optional[str] = None
    subdiagram_name: Optional[str] = None


@dataclass
class DataProcess:
    id: str
    name: str
    lib_name: str
    table_name: str
