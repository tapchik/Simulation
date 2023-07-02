from dataclasses import dataclass
from enum import Enum
from motive import motive

class MOTIVES(Enum):
    Sleep = 'Сон'
    Hunger = 'Голод'
    Entertainment = 'Развлечение'
    Hygiene = 'Гигиена'

default_motives = [
    motive(MOTIVES.Sleep, 85, 1/16/60),
    motive(MOTIVES.Hunger, 75, 3/24/60),
    motive(MOTIVES.Entertainment, 75, 3/24/60),
    motive(MOTIVES.Hygiene, 80, 1/16/60),
]