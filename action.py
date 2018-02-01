import pyautogui
import re

from time import sleep
import copy

from log import log

import helper
from config import config

# constants move to config
travel_title_pos = config["main"]["travel_title_pos"]
end_travel_title_pos = config["main"]["end_travel_title_pos"]

lock_target_pos = config["main"]["lock_target_pos"]

active_eve_pos = config["main"]["active_eve_pos"]
copy_target_data_pos = config["main"]["copy_target_data_pos"]
align_target_pos = config["main"]["align_target_pos"]

warp_bar_pos = config["main"]["warp_bar_pos"]
gate_bar_pos = config["main"]["gate_bar_pos"]

drone_in_bay_pos = config["main"]["drone_in_bay_pos"]

item_bar_end_y = config["main"]["item_bar_end_y"][1]
anomaly_list_end_y = config["main"]["anomaly_list_end_y"][1]

journal_button_pos = config["main"]["journal_button_pos"]
journal_close_button_pos = config["main"]["journal_close_button_pos"]
journal_expeditions_pos = config["main"]["journal_expeditions_pos"]
expeditions_item_pos = config["main"]["expeditions_item_pos"]
expeditions_list_end_y = config["main"]["expeditions_list_end"][1]


# ship constant
optimal_distance = config["combat"]["optimal_distance"]  # km

anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]

jam_mobs_name = config["combat"]["jam_mobs_name"]

max_speed = config["ship"]["max_speed"]  # m/s
speed_module_pos = config["ship"]["speed_module_pos"]

sub_modules_pos_1 = config["ship"]["sub_modules_pos_1"]
sub_modules_pos_2 = config["ship"]["sub_modules_pos_2"]
sub_modules_pos_3 = config["ship"]["sub_modules_pos_3"]

warp_to_anomaly_timeout = config["ship"]["timeout"]["warp_to_anomaly"]

# fight
bar_item_pos = config["main"]["bar_item_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]

accept_mission_pos = config["mission"]["accept_mission_pos"]
agent_start_conversation_pos = config["mission"]["agent_start_conversation_pos"]
mission_title_pos = config["mission"]["mission_title_pos"]
close_mission_pos = config["mission"]["close_mission_pos"]
mission_path_pos = config["mission"]["mission_path_pos"]


undock_pos = config["main"]["undock_pos"]
grid_bar_pos = config["main"]["grid_bar_pos"]


def active_eve():
    pyautogui.moveTo(*active_eve_pos, duration=1.0)
    pyautogui.click()


def get_target_data(target_pos=copy_target_data_pos):
    pyautogui.moveTo(*target_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.2)
    pyautogui.click(interval=0.2)

    clipboard_data = helper.get_data_from_clipboard()

    return clipboard_data


def parse_target_data(data):
    if data is None or len(data) == 0:
        return {
            "name": "empty",
            "distance": "0 m"
        }

    infos = data.split("<br>")

    result = dict()
    result["name"] = infos[0]

    if len(infos) > 1:
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

    try:
        distance = distance[:-metric_len].replace(str(chr(160)), "")
        distance = distance.replace(",", "")
        info["number"] = int(distance)

        log.info('Distance info: ' + str(info["number"]))
    except ValueError:
        pass

    return info


def fly_to_target(distance, opt_distance=optimal_distance, speed=max_speed):
    pyautogui.moveTo(*speed_module_pos, duration=0.5)
    pyautogui.click()

    is_target_exist = True

    while True:
        pyautogui.moveTo(*align_target_pos, duration=0.5)
        pyautogui.click()

        wait_time = (distance - opt_distance) / (speed * 2)
        log.info("estimated flying time: " + str(wait_time) + ' sec')
        if wait_time > 0:
            sleep(wait_time)

        target_info = parse_target_data(get_target_data())

        log.info('Current target info: ' + str(target_info))

        if target_info['name'] == 'empty':
            is_target_exist = False
            break

        target_distance = parse_distance(target_info["distance"])

        if distance <= opt_distance:
            break

        distance = target_distance["number"]
        if target_distance["metric"] == "km":
            distance *= 1000

    pyautogui.moveTo(*speed_module_pos, duration=0.25)
    pyautogui.click()
    return is_target_exist


def destroy_target(with_periscope_drones=False, periscope_timeout=0):
    delta_time = 0
    sleep_time = 3

    target_info = parse_target_data(get_target_data())

    is_need_reactivate_lock = False
    for mob in jam_mobs_name:
        if mob in target_info["name"]:
            is_need_reactivate_lock = True
            break

    current_target_name = target_info['name']
    while True:
        sleep(sleep_time)
        delta_time += sleep_time

        log.info('Target info: ' + str(target_info))
        if target_info["name"] == "empty" or target_info['name'] != current_target_name:
            break

        if is_need_reactivate_lock:
            click_pos(lock_target_pos)

        if with_periscope_drones and delta_time >= periscope_timeout:
            delta_time = 0
            pyautogui.press('r', pause=40)

        # press F
        pyautogui.press('l', pause=3)
        pyautogui.press('f')

        target_info = parse_target_data(get_target_data())

    pyautogui.press('r', pause=5)


def jump_through_gate():
    pyautogui.moveTo(*travel_title_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.2)
    pyautogui.click()


def get_jump_title_data():
    pyautogui.moveTo(*travel_title_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.2)
    pyautogui.click()

    return helper.get_data_from_clipboard()


def init_gate_warp():
    click_pos(warp_bar_pos)
    click_pos(bar_item_pos)


def click_pos(click_target_pos, duration=0.5, pause=0.1):
    pyautogui.moveTo(*click_target_pos, duration=duration)
    pyautogui.click(pause=pause)


def find_item_in_bar(bar_pos, item_names, start_item_pos=bar_item_pos):
    click_pos(bar_pos)

    item_pos = copy.deepcopy(start_item_pos)
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

        for item in item_names:
            if item in target_info["name"]:
                return item_pos

        item_pos[1] = item_pos[1] + 19

        if item_pos[1] > item_bar_end_y:
            return None


def copy_data_from_pos(pos):
    click_pos(pos, pause=1)
    pyautogui.hotkey('ctrl', 'c', interval=0.2, pause=0.5)

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


def find_anomaly_pos(anomaly_init_pos, anomaly_list, except_anomaly_ids):
    anomaly_pos = copy.deepcopy(anomaly_init_pos)

    prev_anomaly_id = ''
    while True:
        anomaly_data = copy_data_from_pos(anomaly_pos)
        anomaly_info = parse_anomaly_data(anomaly_data)

        if len(anomaly_info) == 4:
            if prev_anomaly_id == anomaly_info['id']:
                return None, None
            prev_anomaly_id = anomaly_info['id']

            for anomaly_name in anomaly_list:
                if anomaly_name == anomaly_info['name']:
                    is_excepted = False
                    for except_id in except_anomaly_ids:
                        if except_id == anomaly_info['id']:
                            is_excepted = True
                            break
                    if not is_excepted:
                        return anomaly_pos, anomaly_info

        anomaly_pos[1] = anomaly_pos[1] + 20
        if (anomaly_pos[1] > anomaly_list_end_y) or len(anomaly_info) == 0:
            return None, None


def check_warp_end(bar_pos):
    click_pos(drone_in_bay_pos)
    drone_in_bay_info = parse_target_data(get_target_data())

    log.init_time()

    click_pos(bar_pos)
    while True:
        click_pos(bar_item_pos)
        target_data = parse_target_data(get_target_data())

        if target_data is not None and drone_in_bay_info['name'] != target_data['name']:
            sleep(helper.get_random_delay(3, 8))
            break

        sleep(helper.get_random_delay(3, 8))

        if log.elapsed_time() > warp_to_anomaly_timeout:
            return False, target_data

    return True, target_data


def click_sub_modules():
    click_pos(sub_modules_pos_1)
    click_pos(sub_modules_pos_2)
    click_pos(sub_modules_pos_3)


def get_mission_from_agent(agent_pos):
    click_pos(agent_pos)

    #click_pos(request_miss_from_agent_pos)
    sleep(helper.get_random_delay(1, 3))

    # get mission name
    return 'Cargo Delivery Objectives'


def parse_expedition_data(data):
    # 7 hours, 40 minutes and 33 seconds	2018.01.29 01:54:00	Gulmorogod	21	Serpentis Narcotic Warehouses
    expedition_info = dict()

    if data is None:
        return expedition_info

    data_list = re.split(r'\t+', data)

    if len(data_list) >= 5:
        expedition_info['time'] = data_list[0]
        expedition_info['date'] = data_list[1]
        expedition_info['system_name'] = data_list[2]
        expedition_info['jump_count'] = data_list[3]
        expedition_info['name'] = data_list[4]

    return expedition_info


def get_end_jump_title_data():
    pyautogui.moveTo(*end_travel_title_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.2)
    pyautogui.click()

    return helper.get_data_from_clipboard()


def parse_path_data(path_data):
    empty_path = {
        'name': 'empty',
        'security_status': 42
    }

    if path_data is None or len(path_data) == 0:
        return empty_path

    result_object = dict()

    start_sys_prefix = "'Current Destination'>"
    start_sys_index = path_data.find(start_sys_prefix)
    end_sys_index = path_data.find("</url>")

    if start_sys_index > -1 and end_sys_index > -1:
        result_object['name'] = path_data[start_sys_index + len(start_sys_prefix): end_sys_index]

    start_sec_prefix = "<hint='Security status'>"
    start_sec_index = path_data.find(start_sec_prefix)
    end_sec_index = path_data.find("</hint>")

    try:
        if start_sec_index > -1 and end_sec_index > -1:
            result_object['security_status'] = float(path_data[start_sec_index + len(start_sec_prefix): end_sec_index])
    except ValueError:
        pass

    return result_object


def set_expedition_path(expedition_pos):
    pyautogui.moveTo(*expedition_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 30, duration=0.2)
    pyautogui.click()


def set_expedition_destination():
    click_pos(journal_button_pos)
    click_pos(journal_expeditions_pos)

    expedition_pos = copy.deepcopy(expeditions_item_pos)

    while True:
        expedition_data = copy_data_from_pos(expedition_pos)

        set_expedition_path(expedition_pos)
        path_data = get_end_jump_title_data()

        expedition_info = parse_expedition_data(expedition_data)
        expedition_path_info = parse_path_data(path_data)

        if 'security_status' in expedition_path_info and expedition_path_info['security_status'] >= 0.5:
            click_pos(journal_close_button_pos)
            return expedition_pos, expedition_info

        expedition_pos[1] = expedition_pos[1] + 20

        if (expedition_pos[1] > expeditions_list_end_y) or len(expedition_info) == 0:
            return None, None


def warp_to_ded_complex(expedition_pos):
    click_pos(journal_button_pos)
    click_pos(journal_expeditions_pos, pause=0.6)

    pyautogui.moveTo(*expedition_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.2)
    pyautogui.click()

    click_pos(journal_close_button_pos)
    click_pos(anomaly_info_close_pos)

    check_warp_end(gate_bar_pos)


def get_mission_title():
    sleep(5)
    pyautogui.moveTo(*mission_title_pos, duration=0.5)
    pyautogui.dragRel(0, 30, 0.3, button='left')

    pyautogui.hotkey('ctrl', 'c', interval=0.2, pause=0.5)

    clipboard_data = helper.get_data_from_clipboard()

    return clipboard_data


def get_mission_from_agent():
    click_pos(agent_start_conversation_pos)

    mission_name = get_mission_title()

    click_pos(accept_mission_pos)

    sleep(5)
    click_pos(close_mission_pos)

    return mission_name


def undock():
    click_pos(undock_pos)

    sleep(20)


def set_mission_destination():
    click_pos(mission_path_pos)
    pyautogui.moveRel(0, 120, duration=0.6)

    pyautogui.click()


def get_grid_info(current_target):
    click_pos(grid_bar_pos)
    click_pos(bar_item_pos)

    sleep(2)

    target_data = parse_target_data(get_target_data())

    return target_data['name'] != current_target['name'], target_data


mission_name = "Cargo Delivery Objectives\n"


#exp_data = '7 hours, 40 minutes and 33 seconds	2018.01.29 01:54:00	Gulmorogod	21	Serpentis Narcotic Warehouses'
#res = parse_expedition_data(exp_data)
#path_data = "<center><url=showinfo:5//30000142 alt='Current Destination'>Jita</url></b> <color=0xff4cffccL><hint='Security status'>0.9</hint></color><fontsize=12><fontsize=8> </fontsize>&lt;<fontsize=8> </fontsize><url=showinfo:4//20000020>Kimotoro</url><fontsize=8> </fontsize>&lt;<fontsize=8> </fontsize><url=showinfo:3//10000002>The Forge</url>"
#res = parse_path_data(path_data)