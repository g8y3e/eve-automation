from config import config

import action

from mission import Mission

struct_bar_pos = config["main"]["struct_bar_pos"]

class CargoDelivery(Mission):
    def start(self):
        item_pos = action.find_item_in_bar(struct_bar_pos, ['Warehouse'])
        if item_pos is not None:
            action.click_pos(item_pos)