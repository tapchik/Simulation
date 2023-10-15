from typing import Any
import yaml


class Translation(dict):
    
    def __getitem__(self, __key: Any) -> Any:
        if __key in self:
            return super().__getitem__(__key)
        else:
            return None

    def add_translation(self, filepath: str) -> None:
        with open(filepath, encoding="utf8") as fh:
            translation = yaml.load(fh, Loader=yaml.FullLoader)
        for key, word in translation['translation'].items():
            self[key] = word


if __name__ == '__main__':
    t = Translation()
    # t.add_translation('translation/russian.yml')
    # print(t['bladder'])
    # print(t['kek'])
