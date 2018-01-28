from process import Process

from log import log
from config import config

import action

anomaly_init_pos = config["main"]["anomaly_pos"]
anomaly_warp_x = config["main"]["anomaly_warp_x"][0]
anomaly_name_list = config["combat"]["anomaly_name"]
anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]


class WarpToAnomaly(Process):
    def __init__(self):
        self._is_anomaly_end = False
        self._is_anomaly_closed = False

    def is_anomaly_end(self):
        return self._is_anomaly_end

    def is_anomaly_closed(self):
        return self._is_anomaly_closed

    def start(self):
        log.init_time()
        log.info('# start warp to anomaly')

        self._is_anomaly_closed = False

        anomaly_pos, anomaly_name = action.find_anomaly_pos(anomaly_init_pos, anomaly_name_list)
        if anomaly_pos is not None:
            log.info('found anomaly - start warping')
            anomaly_pos[0] = anomaly_warp_x
            action.click_pos(anomaly_pos)

            if 'drone' in anomaly_name.lower():
                action.click_pos(anomaly_info_close_pos)

            warp_result = action.check_warp_end()

            if not warp_result:
                self._is_anomaly_closed = True
        else:
            self._is_anomaly_end = True

        log.info('# elapsed time: ' + str(log.elapsed_time()) + ' sec')
        log.info('# end warp to anomaly')
