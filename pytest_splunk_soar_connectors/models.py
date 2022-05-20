from dataclasses import dataclass
import random
from typing import Any, Dict, List, Literal, Optional, TypedDict
from typing_extensions import NotRequired
import uuid
import datetime
import sys

@dataclass
class Container:
    id: int

class Artifact(TypedDict):
    name: str
    label: str
    create_time: datetime.datetime
    start_time: datetime.datetime
    end_time: Optional[datetime.datetime]
    severity: Literal['low', 'medium', 'high']
    type: NotRequired[str]
    kill_chain: NotRequired[str]
    hash: str
    cef: Dict[str, Any]
    container: int
    tags: NotRequired[List[str]]
    data: Dict
    id: Optional[int]
    source_data_identifier: Optional[str]
    version: NotRequired[int]
