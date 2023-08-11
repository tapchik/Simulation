from dataclasses import dataclass

@dataclass
class advertisement(dict):
    id: str
    action: str
    motive: str
    status: str
    message_start: str | None
    message_end: str | None
    fulfills: int # 100 is max
    duration: int # measured in ticks