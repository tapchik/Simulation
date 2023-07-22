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

def read_advertisements(filepath: str) -> dict[str, sim.advertisement]:
    assert fileExists(filepath), f"File '{filepath}' was not found, can't load objects for simulation"
    advertisements: dict[str, sim.advertisement] = {}
    with open(filepath, encoding="utf8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
        for ad_id, item in read_data['advertisements'].items():
            advertisement = _assemble_advertisement(item)
            advertisements[ad_id] = advertisement
    return advertisements
