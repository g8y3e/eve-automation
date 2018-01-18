import log
import action

from process import Process

from config import Config
config = Config().get()

lock_target_pos = config["main"]["lock_target_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]
enemy_pos = config["main"]["bar_item_pos"]

missile_module_pos = config["ship"]["missile_module_pos"]


class KillEnemy(Process):
    def start(self):
        action.click_pos(enemy_bar_pos)
        log.info('# start killing enemies')

        while True:
            action.click_pos(enemy_pos)

            target_info = action.parse_target_data(action.get_target_data())
            target_distance = action.parse_distance(target_info["distance"])

            log.info('target name: ' + target_info["name"])

            if target_info["name"] == "empty":
                break

            if target_distance["metric"] == "km" and target_distance["number"] > action.optimal_distance:
                action.fly_to_target(target_distance["number"])

            log.info('lock target')
            action.click_pos(lock_target_pos)

            #action.click_pos(missile_module_pos)

            log.info('killing target')
            action.destroy_target()

        log.info('# end killing enemies')