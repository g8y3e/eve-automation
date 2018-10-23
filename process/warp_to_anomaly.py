from process import Process

from log import log
from config import config

import action

anomaly_init_pos = config["main"]["anomaly_pos"]
anomaly_warp_x = config["main"]["anomaly_warp_x"][0]
anomaly_name_list = config["combat"]["anomaly_name"]
anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]

enemy_bar_pos = config["main"]["enemy_bar_pos"]
grid_bar_pos = config["main"]["grid_bar_pos"]


class WarpToAnomaly(Process):
    def __init__(self):
        self._is_anomaly_end = False
        self._is_anomaly_closed = False
        self._except_anomaly_ids = []

    def is_anomaly_end(self):
        return self._is_anomaly_end

    def is_anomaly_closed(self):
        return self._is_anomaly_closed

    def get_except_anomaly_ids(self):
        return self._except_anomaly_ids

    def start(self):
        log.init_time()
        log.info('# start warp to anomaly')

        self._is_anomaly_closed = False

        anomaly_pos, anomaly_info = action.find_anomaly_pos(anomaly_init_pos, anomaly_name_list, self._except_anomaly_ids)
        if anomaly_pos is not None:
            log.info('found anomaly - start warping')
            anomaly_pos[0] = anomaly_warp_x
            action.click_pos(anomaly_pos)

            if 'drone' in anomaly_info['name'].lower():
                action.click_pos(anomaly_info_close_pos)

            warp_result, target_data = action.check_warp_end(enemy_bar_pos)

            is_someone_in_grid, grid_data = action.get_grid_info(target_data)
            if is_someone_in_grid:
                log.info('have someone in anomaly with name: ' + grid_data['name'])
                self._is_anomaly_closed = True
                self._except_anomaly_ids.append(anomaly_info['id'])

            if not warp_result:
                self._is_anomaly_closed = True
        else:
            self._is_anomaly_end = True

        log.info('# elapsed time: ' + str(log.elapsed_time()) + ' sec')
        log.info('# end warp to anomaly')
