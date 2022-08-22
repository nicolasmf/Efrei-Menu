from dataclasses import dataclass, field
from typing import List
from Grade import Grade


@dataclass
class Subject:
    name: str
    mean: float
    grades: List[Grade]
