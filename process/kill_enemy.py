from log import log
import action

from process import Process

from config import config

lock_target_pos = config["main"]["lock_target_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]
enemy_pos = config["main"]["bar_item_pos"]

attack_module_pos = config["ship"]["attack_module_pos"]
anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]

rare_ship_name = config["combat"]["rare_ship_name"]


class KillEnemy(Process):
    def __init__(self):
        self._is_killed_rare_ship = False

    def is_killed_rare_ship(self):
        self._is_killed_rare_ship

    def start(self):
        action.click_pos(enemy_bar_pos)
        log.init_time()
        log.info('# start killing enemies')

        # activate sub module
        action.click_sub_modules()

        while True:
            action.click_pos(enemy_pos)

            target_info = action.parse_target_data(action.get_target_data())
            if 'distance' in target_info:
                target_distance = action.parse_distance(target_info["distance"])

                log.info('\ntarget name: ' + target_info["name"])

                if target_info["name"] == "empty" or 'metric' not in target_distance:
                    break

                is_target_exist = True
                if target_distance["metric"] == "km" and target_distance["number"] * 1000 > action.optimal_distance:
                    is_target_exist = action.fly_to_target(target_distance["number"] * 1000)

                if is_target_exist:
                    log.info('lock target')
                    action.click_pos(lock_target_pos)

                    action.click_pos(attack_module_pos)

                    log.info('killing target')
                    action.destroy_target()

                    for rare_name in rare_ship_name:
                        if rare_name in target_info["name"]:
                            self._is_killed_rare_ship = True
            else:
                break

        # de-activate sub modules
        action.click_sub_modules()
        action.click_pos(anomaly_info_close_pos)

        log.info('# elapsed time: ' + str(log.elapsed_time()) + ' sec')
        log.info('# end killing enemies')