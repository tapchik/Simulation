from os.path import exists as fileExists
import yaml
import simulation as sim

def _assemble_advertisement(input: dict) -> sim.advertisement: 
    option = sim.advertisement(
        action=input['action'], 
        motive=input['motive'],
        status=input['status'],
        message_start=input['message_start'],
        message_end=input['message_end'], 
        fulfills=input['fulfills'],
        duration=input['duration']
    )
    return option

def read_advertisements(filepath: str) -> list[sim.advertisement]:
    assert fileExists(filepath), f"File '{filepath}' was not found, can't load objects for simulation"
    advertisements: list[sim.advertisement] = []
    with open(filepath, encoding="utf8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
        for item in read_data['options']:
            advertisement = _assemble_advertisement(item)
            advertisements += [advertisement]
    return advertisements
