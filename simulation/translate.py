from typing import Any
import yaml

class translate(dict):
    def __init__(self, filepath: str):
        with open(filepath, encoding="utf8") as fh:
            translation = yaml.load(fh, Loader=yaml.FullLoader)
        for key, word in translation['translation'].items():
            self[key] = word
    
    def __getitem__(self, __key: Any) -> Any:
        if __key in self:
            return super().__getitem__(__key)
        else:
            return None
        
if __name__=='__main__':
    t = translate('translation/russian.yml')
    print(t['bladder'])
    print(t['kek'])