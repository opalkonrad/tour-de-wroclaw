from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel


class AttractionNode(BaseModel):
    id: int
    name: Optional[str]
    pos: Tuple[float, float]


class GraphPath(BaseModel):
    edges: List[int]
    length: float


class AttractionsPair(BaseModel):
    start: AttractionNode
    end: AttractionNode
    bike_path: Optional[GraphPath]
    safer_bike_path: Optional[GraphPath]
    other_path: Optional[GraphPath]


class PairsList(BaseModel):
    pairs: List[AttractionsPair]
