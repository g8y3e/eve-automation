import pyautogui

from time import sleep

import helper
from config import Config
config = Config().get()

# constants move to config
travel_pos = config["main"]["travel_pos"]
travel_title_pos = config["main"]["travel_title_pos"]

active_eve_pos = config["main"]["active_eve_pos"]
copy_target_data_pos = config["main"]["copy_target_data_pos"]
align_target_pos = config["main"]["align_target_pos"]

warp_bar_pos = config["main"]["warp_bar_pos"]
warp_gate_pos = config["main"]["bar_item_pos"]

# ship constant
optimal_distance = config["combat"]["optimal_distance"]  # km

max_speed = config["ship"]["max_speed"]  # m/s
speed_module_pos = config["ship"]["speed_module_pos"]


def active_eve():
    pyautogui.moveTo(*active_eve_pos, duration=1.0)
    pyautogui.click()


def get_target_data():
    pyautogui.moveTo(*copy_target_data_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.5)
    pyautogui.click()

    return helper.get_data_from_clipboard()


def parse_target_data(data):
    if data is None:
        return {
            "name": "empty",
            "distance": "0 m"
        }

    infos = data.split("<br>")
    print(infos)

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


def fly_to_target(distance, opt_distance=optimal_distance, max_speed=max_speed):
    pyautogui.moveTo(*speed_module_pos, duration=0.5)
    pyautogui.click()

    while True:
        pyautogui.moveTo(*align_target_pos, duration=0.5)
        pyautogui.click()

        wait_time = ((distance - opt_distance) * 1000) / (max_speed * 2)
        if wait_time > 0:
            sleep(wait_time)

        target_info = parse_target_data(get_target_data())
        target_distance = parse_distance(target_info["distance"])

        if target_distance["metric"] != "km":
            break

        distance = target_distance["number"]

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


def click_pos(click_pos):
    pyautogui.moveTo(*click_pos, duration=0.5)
    pyautogui.click()

