import sys
import threading
from time import sleep

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import action
import helper
from config import config
from config import config_save

from process.kill_enemy import KillEnemy
from process.travel import Travel
from process.loot_wreck import LootWreck
from process.warp_to_anomaly import WarpToAnomaly

warp_bar_pos = config["main"]["warp_bar_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]
wreck_bar_pos = config["main"]["wreck_bar_pos"]
warp_dock_loot_pos = config["main"]["warp_dock_loot_pos"]
align_target_pos = config["main"]["align_target_pos"]
lock_target_pos = config["main"]["lock_target_pos"]
anomaly_pos = config["main"]["anomaly_pos"]


active_eve_pos = config["main"]["active_eve_pos"]

config_label = {
    'Warp Bar': ['main', 'warp_bar_pos'],
    'Enemy Bar': ['main', 'enemy_bar_pos'],
    'Wreck Bar': ['main', 'wreck_bar_pos'],
    'Warp Dock Loot': ['main', 'warp_dock_loot_pos'],
    'Align': ['main', 'align_target_pos'],
    'Lock Target': ['main', 'lock_target_pos'],
    'Anomaly': ['main', 'anomaly_pos'],

    'Eve Window': ['main', 'active_eve_pos'],
}

# anomaly time
# Drone Cluster - 5m 38s
# Guristas Hideaway - 5m 14s, 2m 7s


class MouseThread(threading.Thread):
    def __init__(self, parent, x_pos_label, y_pos_label):
        threading.Thread.__init__(self)
        self.x_pos_label = x_pos_label
        self.y_pos_label = y_pos_label
        self.killed = False

    def run(self):
        sleep(3)
        try:
            while True:
                if self.stopped():
                    break
                pos = helper.get_mouse_pos()

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

        self._current_button_pressed = ''
        self._label_for_button = dict()

        helper.clear_clipboard()

        self.set_border_width(10)

        window_size = config["window"]["size"]
        self.set_default_size(*window_size)

        screen_size = helper.get_screen_size()
        self.move(screen_size[0] / 2 - window_size[0] / 2, screen_size[1] / 2 - window_size[1] / 2)

        self.connect("destroy", self.quit)

        # connect the key-press event - this will call the keypress
        # handler when any key is pressed
        self.connect("key-press-event", self.on_key_press_event)

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

        #self.add(hbox)

        grid = Gtk.Grid()
        self.add(grid)

        bar_pos_label = Gtk.Label("Item bar positions:\n")
        grid.add(bar_pos_label)

        helper.create_pos_group(grid, 1, 'Warp Bar', warp_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(grid, 2, 'Enemy Bar', enemy_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(grid, 3, 'Wreck Bar', wreck_bar_pos, self.on_button_clicked, self._label_for_button)

        navigation_label = Gtk.Label("\n\nNavigation buttons:\n")
        grid.attach(navigation_label, 0, 4, 1, 1)

        helper.create_pos_group(grid, 5, 'Warp Dock Loot', warp_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(grid, 6, 'Align', align_target_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(grid, 7, 'Lock Target', lock_target_pos, self.on_button_clicked, self._label_for_button)

        navigation_label = Gtk.Label("\n\nGUI buttons:\n")
        grid.attach(navigation_label, 0, 8, 1, 1)

        helper.create_pos_group(grid, 9, 'Anomaly', warp_bar_pos, self.on_button_clicked, self._label_for_button)

        init_label = Gtk.Label("\n\nInit:\n")
        grid.attach(init_label, 0, 10, 1, 1)
        helper.create_pos_group(grid, 11, 'Eve Window', active_eve_pos, self.on_button_clicked, self._label_for_button)

        empty_label = Gtk.Label("\n\n\n")
        grid.attach(empty_label, 0, 12, 1, 1)
        helper.create_pos_group(grid, 13, 'Start Game', active_eve_pos, self.on_button_start, self._label_for_button)

        self.mouseThread = MouseThread(self, self.x_pos_label, self.y_pos_label)
        self.mouseThread.start()

    def on_button_start(self, widget):
        action.active_eve()

        warp = WarpToAnomaly()
        warp.start()
        while not warp.is_anomaly_end():
            kill = KillEnemy()
            kill.start()

            loot_wreck = LootWreck()
            loot_wreck.start()

            warp.start()

        travel = Travel()
        travel.set_iter_jump()
        while not travel.is_path_end():
            travel.start()

            warp = WarpToAnomaly()
            warp.start()
            while not warp.is_anomaly_end():
                kill = KillEnemy()
                kill.start()

                loot_wreck = LootWreck()
                loot_wreck.start()

                warp.start()

    def on_button_clicked(self, widget):
        print("Hello World" + widget.get_label())

        self._current_button_pressed = widget.get_label()

    def on_key_press_event(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # see if we recognise a keypress
        if event.keyval == Gdk.KEY_q:
            self.quit(widget)

        if event.keyval == Gdk.KEY_s:
            self.save_mouse_pos()

    def save_mouse_pos(self):
        current_pos = helper.get_mouse_pos()

        if self._current_button_pressed in config_label:
            config_path = config_label[self._current_button_pressed]
            item = config
            for index_name in config_path:
                item = item[index_name]

            item[0] = current_pos[0]
            item[1] = current_pos[1]

            config_save()

            if self._current_button_pressed in self._label_for_button:
                attached_pos_label = self._label_for_button[self._current_button_pressed]
                attached_pos_label.set_text(helper.convert_pos_to_str(item))

    def quit(self, widget):
        self.mouseThread.kill()
        Gtk.main_quit()

win = EVEWindow(config["window"]["title"])

win.show_all()
Gtk.main()
