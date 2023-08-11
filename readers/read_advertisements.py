from os.path import exists as fileExists
import yaml
import simulation as sim

def _assemble_advertisement(id:str, input: dict) -> sim.advertisement: 
    option = sim.advertisement(
        id=id,
        action=input['action'], 
        motive=input['motive'],
        status=input['status'],
        message_start=input['message_start'],
        message_end=input['message_end'], 
        fulfills=input['fulfills'],
        duration=input['duration'], 
    )
    option['started']=input['started'] if 'started' in input else {'message': None, 'sound': {'anyone': None}}
    option['finished']=input['finished'] if 'finished' in input else {'message': None, 'sound': {'anyone': None}}
    return option

def read_advertisements(filepath: str) -> dict[str, sim.advertisement]:
    assert fileExists(filepath), f"File '{filepath}' was not found, can't load objects for simulation"
    advertisements: dict[str, sim.advertisement] = {}
    with open(filepath, encoding="utf8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
        for ad_id, item in read_data['advertisements'].items():
            advertisement = _assemble_advertisement(ad_id, item)
            advertisements[ad_id] = advertisement
    return advertisements
