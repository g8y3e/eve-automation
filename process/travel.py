from time import sleep

from process import Process

import log

import helper
import action
from config import Config
config = Config().get()

warp_pos = config["main"]["warp_dock_pos"]


class Travel(Process):
    def __init__(self):
        self._is_iter_jump = False

    def _check_travel_data(self, data):
        return data is not None and data.lower() != "no destination"

    def set_iter_jump(self):
        self._is_iter_jump = True

    def start(self):
        log.info('# start travel process!')
        helper.clear_clipboard()
        clipboard_data = action.get_jump_title_data()

        if self._check_travel_data(clipboard_data):
            log.info('has destination path')
            prev_system = clipboard_data
            # check warp bar
            action.init_gate_warp()

            while True:
                action.click_pos(warp_pos)

                warp_delay = helper.get_random_delay(8, 15)
                log.info('warping with delay: ' + str(warp_delay) + ' sec')
                sleep(warp_delay)

                helper.clear_clipboard()
                clipboard_data = action.get_jump_title_data()
                if clipboard_data is not None and clipboard_data.lower() == "no destination":
                    break

                if clipboard_data is not None and prev_system != clipboard_data and self._is_iter_jump:
                    break

        log.info('# end travel process!')

# TFL-699	Cosmic Anomaly	Combat Site	Guristas Hidden Hideaway	100.0%	10.96 AU