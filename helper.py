import pyautogui
from random import randint

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


def get_screen_size():
    return pyautogui.size()


def get_mouse_pos():
    return pyautogui.position()


def get_data_from_clipboard():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    return clipboard.wait_for_text()


def clear_clipboard():
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.clear()


def get_random_delay(min, max):
    return randint(min, max)


def convert_pos_to_str(pos):
    return '   x: ' + str(pos[0]) + '; y: ' + str(pos[1]) + ';  '


def create_pos_group(layout, index, button_name, current_pos, callback, attach_label):
    button = Gtk.Button(label=button_name)

    label = Gtk.Label(convert_pos_to_str(current_pos))
    layout.attach(button, 0, index, 1, 1)
    layout.attach_next_to(label, button, Gtk.PositionType.RIGHT, 2, 1)

    button.connect("clicked", callback)

    attach_label[button_name] = label