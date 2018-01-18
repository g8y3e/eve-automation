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