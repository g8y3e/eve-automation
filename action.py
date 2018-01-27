import pyautogui
import re

from time import sleep
import copy

from log import log

import helper
from config import config

# constants move to config
travel_title_pos = config["main"]["travel_title_pos"]

active_eve_pos = config["main"]["active_eve_pos"]
copy_target_data_pos = config["main"]["copy_target_data_pos"]
align_target_pos = config["main"]["align_target_pos"]

warp_bar_pos = config["main"]["warp_bar_pos"]
warp_gate_pos = config["main"]["bar_item_pos"]

drone_in_bay_pos = config["main"]["drone_in_bay_pos"]

item_bar_end_y = config["main"]["item_bar_end_y"][1]
anomaly_list_end_y = config["main"]["anomaly_list_end_y"][1]


# ship constant
optimal_distance = config["combat"]["optimal_distance"]  # km

max_speed = config["ship"]["max_speed"]  # m/s
speed_module_pos = config["ship"]["speed_module_pos"]

sub_modules_pos_1 = config["ship"]["sub_modules_pos_1"]
sub_modules_pos_2 = config["ship"]["sub_modules_pos_2"]
sub_modules_pos_3 = config["ship"]["sub_modules_pos_3"]

# fight
enemy_pos = config["main"]["bar_item_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]


def active_eve():
    pyautogui.moveTo(*active_eve_pos, duration=1.0)
    pyautogui.click()


def get_target_data():
    pyautogui.moveTo(*copy_target_data_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.5)
    pyautogui.click()

    clipboard_data = helper.get_data_from_clipboard()
    print('Current clipboard data: ' + clipboard_data)

    return clipboard_data


def parse_target_data(data):
    if data is None:
        return {
            "name": "empty",
            "distance": "0 m"
        }

    infos = data.split("<br>")

    result = dict()
    result["name"] = infos[0]
    result["distance"] = infos[1].lower().replace("distance: ", "")

    if len(infos) > 2:
        result["bounty"] = infos[2].lower().replace("bounty: ", "")

    return result


def parse_distance(distance):
    info = dict()
    metric_len = 3
    if " km" in distance:
        info["metric"] = "km"
    elif " m" in distance:
        info["metric"] = "m"
        metric_len = 2

    info["number"] = int(distance[:-metric_len].replace(",", ""))

    return info


def fly_to_target(distance, opt_distance=optimal_distance, speed=max_speed):
    pyautogui.moveTo(*speed_module_pos, duration=0.5)
    pyautogui.click()

    while True:
        pyautogui.moveTo(*align_target_pos, duration=0.5)
        pyautogui.click()

        wait_time = (distance - opt_distance) / (speed * 2)
        log.info("estimated flying time: " + str(wait_time) + ' sec')
        if wait_time > 0:
            sleep(wait_time)

        target_info = parse_target_data(get_target_data())
        target_distance = parse_distance(target_info["distance"])

        if distance <= opt_distance:
            break

        distance = target_distance["number"]
        if target_distance["metric"] == "km":
            distance *= 1000

    pyautogui.moveTo(*speed_module_pos, duration=0.25)
    pyautogui.click()


def destroy_target():
    while True:
        sleep(3)

        target_info = parse_target_data(get_target_data())
        if target_info["name"] == "empty":
            break

        # press F
        pyautogui.press('l', pause=3)
        pyautogui.press('f')

    pyautogui.press('r', pause=5)


def jump_through_gate():
    pyautogui.moveTo(*travel_title_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.5)
    pyautogui.click()


def get_jump_title_data():
    pyautogui.moveTo(*travel_title_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.5)
    pyautogui.click()

    return helper.get_data_from_clipboard()


def init_gate_warp():
    click_pos(warp_bar_pos)
    click_pos(warp_gate_pos)


def click_pos(click_pos, duration=0.5, pause=0):
    pyautogui.moveTo(*click_pos, duration=duration)
    pyautogui.click(pause=pause)


def find_item_in_bar(bar_pos, ship_names):
    click_pos(bar_pos)

    item_pos = copy.deepcopy(enemy_pos)
    prev_name = ""
    while True:
        click_pos(item_pos)

        target_info = parse_target_data(get_target_data())

        if len(prev_name) > 0 and prev_name == target_info["name"]:
            click_pos(drone_in_bay_pos)
            drone_in_bay_info = parse_target_data(get_target_data())

            click_pos(item_pos)
            target_info = parse_target_data(get_target_data())

            if drone_in_bay_info["name"] == target_info["name"]:
                return None

        prev_name = target_info["name"]

        for item in ship_names:
            if item in target_info["name"]:
                return item_pos

        item_pos[1] = item_pos[1] + 20

        if item_pos[1] > item_bar_end_y:
            return None


def copy_data_from_pos(pos):
    click_pos(pos, pause=1)
    pyautogui.hotkey('ctrl', 'C', interval=0.2, pause=1)

    return helper.get_data_from_clipboard()


def parse_anomaly_data(data):
    # NPJ-568	Cosmic Anomaly	Combat Site	Guristas Hideaway	100.0%	1.89 AU
    anomaly_info = dict()

    if data is None:
        return anomaly_info

    data_list = re.split(r'\t+', data)

    if len(data_list) >= 5:
        anomaly_info['id'] = data_list[0]
        anomaly_info['type'] = data_list[2]
        anomaly_info['name'] = data_list[3]
        anomaly_info['distance'] = data_list[5]

    return anomaly_info


def find_anomaly_pos(anomaly_init_pos, anomaly_list):
    anomaly_pos = copy.deepcopy(anomaly_init_pos)

    prev_anomaly_id = ''
    while True:
        anomaly_data = copy_data_from_pos(anomaly_pos)
        anomaly_info = parse_anomaly_data(anomaly_data)

        log.info('Current anomaly data: ' + anomaly_data)

        if len(anomaly_info) == 4:
            if prev_anomaly_id == anomaly_info['id']:
                return None, None
            prev_anomaly_id = anomaly_info['id']

            for anomaly_name in anomaly_list:
                if anomaly_name == anomaly_info['name']:
                    return anomaly_pos, anomaly_info['name']

        anomaly_pos[1] = anomaly_pos[1] + 20
        if (anomaly_pos[1] > anomaly_list_end_y) or len(anomaly_info) == 0:
            return None, None


def check_warp_end():
    click_pos(drone_in_bay_pos)
    drone_in_bay_info = parse_target_data(get_target_data())

    click_pos(enemy_bar_pos)
    while True:
        click_pos(enemy_pos)
        target_data = parse_target_data(get_target_data())

        if target_data is not None and drone_in_bay_info['name'] != target_data['name']:
            sleep(helper.get_random_delay(3, 8))
            break

        sleep(helper.get_random_delay(3, 8))


def click_sub_modules():
    click_pos(sub_modules_pos_1)
    click_pos(sub_modules_pos_2)
    click_pos(sub_modules_pos_3)
