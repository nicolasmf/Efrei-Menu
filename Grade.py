from dataclasses import dataclass


@dataclass
class Grade:
    type_: str
    coeff: float
    grade: float
