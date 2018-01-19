import sys
import threading
from time import sleep

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import action
import helper
from config import Config
config = Config().get()

from process.kill_enemy import KillEnemy
from process.travel import Travel
from process.loot_wreck import LootWreck

warp_bar_pos = config["main"]["warp_bar_pos"]


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

        self.add(hbox)

        self.mouseThread = MouseThread(self, self.x_pos_label, self.y_pos_label)
        self.mouseThread.start()

        action.active_eve()

        kill = KillEnemy()
        kill.start()

        travel = Travel()
        travel.set_iter_jump()
        #travel.start()

        lootWreck = LootWreck()
        lootWreck.start()

    def on_button_clicked(self, widget):
        print("Hello World")

    def on_key_press_event(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # see if we recognise a keypress
        if event.keyval == Gdk.KEY_q:
            self.quit(widget)

    def quit(self, widget):
        self.mouseThread.kill()
        Gtk.main_quit()

win = EVEWindow(config["window"]["title"])

win.show_all()
Gtk.main()
