from process import Process

from log import log
from config import config

import action

anomaly_init_pos = config["main"]["anomaly_pos"]
anomaly_warp_dx = config["main"]["anomaly_warp_dx"]
anomaly_name_list = config["combat"]["anomaly_name"]


class WarpToAnomaly(Process):
    def __init__(self):
        self._is_anomaly_end = False

    def is_anomaly_end(self):
        return self._is_anomaly_end

    def start(self):
        log.init_time()
        log.info('# start warp to anomaly')

        anomaly_pos = action.find_anomaly_pos(anomaly_init_pos, anomaly_name_list)
        if anomaly_pos is not None:
            log.info('found anomaly - start warping')
            anomaly_pos[0] += anomaly_warp_dx
            action.click_pos(anomaly_pos)

            action.check_warp_end()
        else:
            self._is_anomaly_end = True

        log.info('# elapsed time: ' + str(log.elapsed_time()) + ' sec')
        log.info('# end warp to anomaly')
