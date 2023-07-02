
from dataclasses import dataclass
from motive import motive

@dataclass
class character: 
    first_name: str
    last_name: str
    age: int
    motives: list[motive]