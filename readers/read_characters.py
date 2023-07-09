from os.path import exists as fileExists
import yaml
import simulation as sim

def _assemble_character(input: dict) -> sim.character:
    assert 'name' in input.keys(), f"Character has to have a 'name' field"
    assert 'sex' in input.keys(), f"Character has to have a 'sex' field"
    assert 'motives' in input.keys(), f"Character has to have a 'motives' field"
    name = input['name']
    sex = input['sex']
    motives = {}
    for title, item in input['motives'].items():
        title = title
        value = item['value'] if 'value' in item else 70
        regularity = item['regularity'] if 'regularity' in item else 1.0
        motive = sim.motive(title, value, regularity)
        motives[title] = motive
    char = sim.character(name, sex, motives)
    return char

def read_characters(filepath: str) -> list[sim.character]:
    assert fileExists(filepath), f"File '{filepath}' was not found, can't load characters for simulation"
    characters: list[sim.character] = []
    with open(filepath, encoding="utf8") as fh:
        read_data = yaml.load(fh, Loader=yaml.FullLoader)
        for item in read_data['characters']:
            char = _assemble_character(item)
            characters += [char]
    return characters