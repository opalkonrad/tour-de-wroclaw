from enum import Enum
from typing import List, Optional, Tuple
from pydantic import BaseModel


class AttractionNode(BaseModel):
    id: int
    name: Optional[str]
    pos: Tuple[float, float]


class Path(BaseModel):
    edges: List[int]
    length: float


class AttractionsPair(BaseModel):
    start: AttractionNode
    end: AttractionNode
    bike_path: Path
    other_path: Path

class PairsList(BaseModel):
    pairs: List[AttractionsPair]
