from dataclasses import dataclass
import simulation as sim

@dataclass
class action:
    
    advertisement: sim.advertisement
    performer: sim.character
    started: int