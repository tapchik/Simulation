from os.path import exists as fileExists
from random import choice
import yaml
import simulation as sim


class AdvertisementRepository(dict[str, sim.advertisement]):

    def chooseAdvertismentToFulfillMotive(self, motive: str | None) -> sim.advertisement | None: 
        all_ads = self.values()
        options = list(filter(lambda ad: ad.motive == motive, all_ads))
        action = choice(options) if options != [] else None
        return action

    def _assemble_advertisement(self, add: dict) -> sim.advertisement:
        option = sim.advertisement(
            action=add['action'],
            motive=add['motive'],
            status=add['status'],
            message_start=add['message_start'],
            message_end=add['message_end'],
            fulfills=add['fulfills'],
            duration=add['duration']
        )
        return option

    def add_advertisments(self, filepath: str) -> None:
        assert fileExists(filepath), f"File '{filepath}' was not found, can't load objects for simulation"
        with open(filepath, encoding="utf8") as fh:
            read_data = yaml.load(fh, Loader=yaml.FullLoader)
            for ad_id, item in read_data['advertisements'].items():
                advertisement = self._assemble_advertisement(item)
                self[ad_id] = advertisement
    
    def add_advertisment(self, ad_id: str, advertisement: sim.advertisement) -> None:
        self[ad_id] = advertisement
