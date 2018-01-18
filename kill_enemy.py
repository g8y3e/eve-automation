import pyautogui

from time import sleep
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

optimal_distance = 40
max_speed = 400 # m/s


def get_target_data():
    copy_text_pos = 1036, 97
    pyautogui.moveTo(*copy_text_pos, duration=0.5)
    pyautogui.click(button='right')

    pyautogui.moveRel(25, 10, duration=0.5)
    pyautogui.click()

    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    return clipboard.wait_for_text()


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


def fly_to_target(distance):
    align_pos = 986, 133
    speed_module_pos = 762, 608

    pyautogui.moveTo(*speed_module_pos, duration=0.5)
    pyautogui.click()

    while True:
        pyautogui.moveTo(*align_pos, duration=0.5)
        pyautogui.click()

        wait_time = ((distance - optimal_distance) * 1000) / max_speed
        if wait_time > 0:
            sleep(wait_time)

        target_info = parse_target_data(get_target_data())
        target_distance = parse_distance(target_info["distance"])

        if target_distance["metric"] != "km":
            break

        distance = target_distance["number"]

    pyautogui.moveTo(*speed_module_pos, duration=0.5)
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

    pyautogui.press('r', pause=10)


class KillEnemy:
    def start(self):
        enemy_bar_pos = 1090, 208
        pyautogui.moveTo(*enemy_bar_pos, duration=0.5)
        pyautogui.click()

        while True:
            enemy_pos = 1092, 246

            pyautogui.moveTo(*enemy_pos, duration=0.5)
            pyautogui.click()

            target_info = parse_target_data(get_target_data())
            target_distance = parse_distance(target_info["distance"])

            if target_info["name"] == "empty":
                break

            if target_distance["metric"] == "km" and target_distance["number"] > optimal_distance:
                fly_to_target(target_distance["number"])

            lock_pos = 1117, 133
            pyautogui.moveTo(*lock_pos, duration=0.5)
            pyautogui.click()

            pos_missile = 812, 607
            pyautogui.moveTo(*pos_missile, duration=0.5)
            pyautogui.click()

            destroy_target()

        t = 53
