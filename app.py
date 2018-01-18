import threading
import sys
from time import sleep

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pyautogui

from kill_enemy import KillEnemy

screen_width, screen_height = pyautogui.size()

window_width = 200
window_height = 100

window_title = "EVE automation"

active_eve_pos = 720, 30


def mousepos():
    return pyautogui.position()


class MouseThread(threading.Thread):
    def __init__(self, parent, x_pos_label, y_pos_label):
        threading.Thread.__init__(self)
        self.x_pos_label = x_pos_label
        self.y_pos_label = y_pos_label
        self.killed = False

    def run(self):
        try:
            while True:
                if self.stopped():
                    break
                pos = mousepos()

                self.x_pos_label.set_text("X: {};".format(pos[0]))
                self.y_pos_label.set_text("Y: {};".format(pos[1]))
                sleep(0.2)
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    def kill(self):
        self.killed = True

    def stopped(self):
        return self.killed


class EVEWindow(Gtk.Window):
    def __init__(self, title):
        Gtk.Window.__init__(self, title=title)

        self.set_border_width(10)
        self.set_default_size(window_width, window_height)
        self.move(screen_width / 2 - window_width / 2, screen_height / 2 - window_height / 2)

        self.connect("destroy", self.quit)

        hbox = Gtk.Box(spacing=10)
        hbox.set_homogeneous(False)

        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_left.set_homogeneous(False)

        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)

        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        self.x_pos_label = Gtk.Label("X: 0;")
        vbox_left.pack_start(self.x_pos_label, True, True, 0)

        self.y_pos_label = Gtk.Label("Y: 0;")
        vbox_right.pack_start(self.y_pos_label, True, True, 0)

        self.add(hbox)

        self.mouseThread = MouseThread(self, self.x_pos_label, self.y_pos_label)
        self.mouseThread.start()

        self.active_eve()

        kill = KillEnemy()
        kill.start()

    def active_eve(self):
        pyautogui.moveTo(*active_eve_pos, duration=1.0)
        pyautogui.click()

    def on_button_clicked(self, widget):
        print("Hello World")

    def quit(self, widget):
        self.mouseThread.kill()
        Gtk.main_quit()

win = EVEWindow(window_title)

win.show_all()
Gtk.main()
