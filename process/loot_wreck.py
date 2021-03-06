from process import Process

import action
from log import log
from config import config

wreck_bar_pos = config["main"]["wreck_bar_pos"]
rare_ship_name = config["combat"]["rare_ship_name"]
loot_distance = config["combat"]["loot_distance"]

loot_pos = config["main"]["warp_dock_loot_pos"]

loot_all_pos = config["main"]["loot_all_pos"]
close_inventory_pos = config["main"]["close_inventory_pos"]


class LootWreck(Process):
    def __init__(self):
        self._rare_ship_name = rare_ship_name

    def set_rare_ship_names(self, ships):
        self._rare_ship_name = ships

    def start(self):
        log.init_time()
        log.info('# start looting wreck')
        item_pos = action.find_item_in_bar(wreck_bar_pos, self._rare_ship_name)

        if item_pos is not None:
            # move to wreck
            log.info('found item position')
            action.click_pos(item_pos)
            target_info = action.parse_target_data(action.get_target_data())
            target_distance = action.parse_distance(target_info["distance"])

            if (target_distance["metric"] == "km" and target_distance["number"] * 1000 > loot_distance) or \
                    (target_distance["metric"] == "m" and target_distance["number"] > loot_distance):
                log.info('flying to wreck')
                if target_distance["metric"] == "km":
                    target_distance["number"] *= 1000

                action.fly_to_target(target_distance["number"], loot_distance)

            log.info('looting items')
            action.click_pos(loot_pos, 2)

            # loot all
            action.click_pos(loot_all_pos, 2)
            action.click_pos(close_inventory_pos)

        log.info('# elapsed time: ' + str(log.elapsed_time()) + ' sec')
        log.info('# end looting wreck')
