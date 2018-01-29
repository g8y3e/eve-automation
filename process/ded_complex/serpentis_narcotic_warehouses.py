from process.ded_complex import DEDComplex

import action

from time import sleep

from config import config
from log import log

from process.kill_enemy import KillEnemy
from process.loot_wreck import LootWreck

enemy_bar_pos = config["main"]["enemy_bar_pos"]
gate_bar_pos = config["main"]["gate_bar_pos"]
struct_bar_pos = config["main"]["struct_bar_pos"]

loot_distance = config["combat"]["loot_distance"]

warp_dock_loot_pos = config["main"]["warp_dock_loot_pos"]
lock_target_pos = config["main"]["lock_target_pos"]
attack_module_pos = config["ship"]["attack_module_pos"]

loot_pos = config["main"]["warp_dock_loot_pos"]

loot_all_pos = config["main"]["loot_all_pos"]
close_inventory_pos = config["main"]["close_inventory_pos"]

anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]


class SerpentisNarcoticWarehouses(DEDComplex):
    def first_stage(self):
        item_pos = action.find_item_in_bar(gate_bar_pos, ['Ancient Acceleration Gate'])

        if item_pos is not None:
            # move to wreck
            log.info('found item position')
            action.click_pos(item_pos)

            action.click_pos(warp_dock_loot_pos)

            action.check_warp_end(enemy_bar_pos)

            action.click_pos(anomaly_info_close_pos)
        else:
            return False

        return True

    def second_stage(self):
        kill_enemy = KillEnemy()
        kill_enemy.start()

        item_pos = action.find_item_in_bar(gate_bar_pos, ['Acceleration Gate to Check-In Tunnel'])

        if item_pos is not None:
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

            action.click_pos(warp_dock_loot_pos)

            action.check_warp_end(enemy_bar_pos)
            action.click_pos(anomaly_info_close_pos)
        else:
            return False

        return True

    def third_stage(self):
        kill_enemy = KillEnemy()
        kill_enemy.start()

        item_pos = action.find_item_in_bar(gate_bar_pos, ['Acceleration Gate to Central Warehouses'])

        if item_pos is not None:
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

            action.click_pos(warp_dock_loot_pos)

            action.check_warp_end(enemy_bar_pos)
            action.click_pos(anomaly_info_close_pos)
        else:
            return False

        return True

    def fourth_stage(self):
        kill_enemy = KillEnemy()
        kill_enemy.start()

        item_pos = action.find_item_in_bar(gate_bar_pos, ['Acceleration Gate to Administration Sector'])

        if item_pos is not None:
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

            action.click_pos(warp_dock_loot_pos)

            action.check_warp_end(enemy_bar_pos)

            action.click_pos(anomaly_info_close_pos)
        else:
            return False

        return True

    def fifth_stage(self):
        item_pos = action.find_item_in_bar(struct_bar_pos, ['Serpentis Supply Stronghold'])
        if item_pos is not None:
            target_info = action.parse_target_data(action.get_target_data())
            target_distance = action.parse_distance(target_info["distance"])

            log.info('\ntarget name: ' + target_info["name"])

            if target_info["name"] == "empty":
                return False

            if target_distance["metric"] == "km" and target_distance["number"] * 1000 > action.optimal_distance:
                action.fly_to_target(target_distance["number"] * 1000)

            log.info('lock target')
            action.click_pos(lock_target_pos)

            action.click_pos(attack_module_pos)

            log.info('killing target')
            action.destroy_target(with_periscope_drones=True, periscope_timeout=60)
            sleep(10)

            action.click_pos(anomaly_info_close_pos)
            container_item_pos = action.find_item_in_bar(struct_bar_pos, ['Cargo Container'])

            while True:
                if container_item_pos is not None:
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

                    break
                else:
                    break

                container_item_pos = action.find_item_in_bar(struct_bar_pos, ['Cargo Container'], start_item_pos=container_item_pos + 18)
        else:
            return False


        return True

    def start(self):
        result = self.first_stage()

        if not result:
            return

        result = self.second_stage()

        if not result:
            return

        result = self.third_stage()

        if not result:
            return

        result = self.fourth_stage()

        if not result:
            return

        self.fifth_stage()