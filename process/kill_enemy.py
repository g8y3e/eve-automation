from log import log
import action

from process import Process

from config import config

lock_target_pos = config["main"]["lock_target_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]
enemy_pos = config["main"]["bar_item_pos"]

attack_module_pos = config["ship"]["attack_module_pos"]
anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]

class KillEnemy(Process):
    def start(self):
        action.click_pos(enemy_bar_pos)
        log.init_time()
        log.info('# start killing enemies')

        # activate sub module
        action.click_sub_modules()

        while True:
            action.click_pos(enemy_pos)

            target_info = action.parse_target_data(action.get_target_data())
            target_distance = action.parse_distance(target_info["distance"])

            log.info('\ntarget name: ' + target_info["name"])

            if target_info["name"] == "empty":
                break

            if target_distance["metric"] == "km" and target_distance["number"] * 1000 > action.optimal_distance:
                action.fly_to_target(target_distance["number"] * 1000)

            log.info('lock target')
            action.click_pos(lock_target_pos)

            action.click_pos(attack_module_pos)

            log.info('killing target')
            action.destroy_target()

        # de-activate sub modules
        action.click_sub_modules()
        action.click_pos(anomaly_info_close_pos)

        log.info('# elapsed time: ' + str(log.elapsed_time()) + ' sec')
        log.info('# end killing enemies')