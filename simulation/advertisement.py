from dataclasses import dataclass

@dataclass
class advertisement:
    action: str
    motive: str
    status: str
    message_start: str
    message_end: str
    fulfills: int # 100 is max
    duration: int # measured in ticks