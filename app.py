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

from process.ded_complex import ded_complex_factory

warp_bar_pos = config["main"]["warp_bar_pos"]
enemy_bar_pos = config["main"]["enemy_bar_pos"]
wreck_bar_pos = config["main"]["wreck_bar_pos"]
warp_dock_loot_pos = config["main"]["warp_dock_loot_pos"]
align_target_pos = config["main"]["align_target_pos"]
lock_target_pos = config["main"]["lock_target_pos"]
anomaly_pos = config["main"]["anomaly_pos"]

journal_button_pos = config["main"]["journal_button_pos"]
journal_close_button_pos = config["main"]["journal_close_button_pos"]
journal_expeditions_pos = config["main"]["journal_expeditions_pos"]
expeditions_item_pos = config["main"]["expeditions_item_pos"]
expeditions_list_end = config["main"]["expeditions_list_end"]
end_travel_title_pos = config["main"]["end_travel_title_pos"]

item_bar_end_y = config["main"]["item_bar_end_y"]

anomaly_list_end_y = config["main"]["anomaly_list_end_y"]
anomaly_warp_x = config["main"]["anomaly_warp_x"]
travel_title_pos = config["main"]["travel_title_pos"]

bar_item_pos = config["main"]["bar_item_pos"]
drone_in_bay_pos = config["main"]["drone_in_bay_pos"]

close_inventory_pos = config["main"]["close_inventory_pos"]
loot_all_pos = config["main"]["loot_all_pos"]

gate_bar_pos = config["main"]["gate_bar_pos"]
struct_bar_pos = config["main"]["struct_bar_pos"]

copy_target_data_pos = config["main"]["copy_target_data_pos"]

attack_module_pos = config["ship"]["attack_module_pos"]
speed_module_pos = config["ship"]["speed_module_pos"]

sub_modules_pos_1 = config["ship"]["sub_modules_pos_1"]
sub_modules_pos_2 = config["ship"]["sub_modules_pos_2"]
sub_modules_pos_3 = config["ship"]["sub_modules_pos_3"]

anomaly_info_close_pos = config["combat"]["anomaly_info_close_pos"]

active_eve_pos = config["main"]["active_eve_pos"]

agent_start_conversation_pos = config["mission"]["agent_start_conversation_pos"]
accept_mission_pos = config["mission"]["accept_mission_pos"]
mission_title_pos = config["mission"]["mission_title_pos"]
close_mission_pos = config["mission"]["close_mission_pos"]
mission_path_pos = config["mission"]["mission_path_pos"]

undock_pos = config["main"]["undock_pos"]

grid_bar_pos = config["main"]["grid_bar_pos"]

config_label = {
    'Warp Bar': ['main', 'warp_bar_pos'],
    'Enemy Bar': ['main', 'enemy_bar_pos'],
    'Wreck Bar': ['main', 'wreck_bar_pos'],
    'Warp Dock Loot': ['main', 'warp_dock_loot_pos'],
    'Align': ['main', 'align_target_pos'],
    'Lock Target': ['main', 'lock_target_pos'],
    'Anomaly': ['main', 'anomaly_pos'],
    'Item Bar End Y': ['main', 'item_bar_end_y'],
    'Anomaly End Y': ['main', 'anomaly_list_end_y'],
    'Anomaly Warp X': ['main', 'anomaly_warp_x'],
    'Travel Title': ['main', 'travel_title_pos'],
    'Bar Item': ['main', 'bar_item_pos'],
    'Drone In Bay': ['main', 'drone_in_bay_pos'],
    'Copy Target Data': ['main', 'copy_target_data_pos'],


    'Close Inventory': ['main', 'close_inventory_pos'],
    'Loot All': ['main', 'loot_all_pos'],

    'Attack Module': ['ship', 'attack_module_pos'],
    'Speed Module': ['ship', 'speed_module_pos'],
    'Sub-Module 1': ['ship', 'sub_modules_pos_1'],
    'Sub-Module 2': ['ship', 'sub_modules_pos_2'],
    'Sub-Module 3': ['ship', 'sub_modules_pos_3'],

    'Anomaly info Close': ['combat', 'anomaly_info_close_pos'],

    'Journal Button': ['main', 'journal_button_pos'],
    'Journal Close Button': ['main', 'journal_close_button_pos'],
    'Journal Expedition': ['main', 'journal_expeditions_pos'],
    'Expedition Item': ['main', 'expeditions_item_pos'],
    'Expedition List End Y': ['main', 'expeditions_list_end'],
    'End Travel Title': ['main', 'end_travel_title_pos'],

    'Gate Bar': ['main', 'gate_bar_pos'],
    'Struct Bar': ['main', 'struct_bar_pos'],
    'Grid Bar': ['main', 'grid_bar_pos'],

    'Agent Start Conversation': ['mission', 'agent_start_conversation_pos'],
    'Accept Mission': ['mission', 'accept_mission_pos'],
    'Mission Title': ['mission', 'mission_title_pos'],
    'Close Mission': ['mission', 'close_mission_pos'],
    'Mission Path': ['mission', 'mission_path_pos'],

    'Undock': ['main', 'undock_pos'],


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
        #self.set_default_size(*window_size)

        screen_size = helper.get_screen_size()

        self.connect("destroy", self.quit)

        # connect the key-press event - this will call the keypress
        # handler when any key is pressed
        self.connect("key-press-event", self.on_key_press_event)

        self.x_pos_label = Gtk.Label("Item bar positions:\n")
        self.y_pos_label = Gtk.Label("Item bar positions:\n")

        main_grid = Gtk.Grid()
        self.add(main_grid)

        first_grid = Gtk.Grid()
        main_grid.attach(first_grid, 0, 0, 1, 1)

        second_grid = Gtk.Grid()
        main_grid.attach(second_grid, 1, 0, 1, 1)

        third_grid = Gtk.Grid()
        main_grid.attach(third_grid, 2, 0, 1, 1)

        bar_pos_label = Gtk.Label("Item bar positions:\n")
        first_grid.add(bar_pos_label)

        helper.create_pos_group(first_grid, 1, 'Warp Bar', warp_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(first_grid, 2, 'Enemy Bar', enemy_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(first_grid, 3, 'Wreck Bar', wreck_bar_pos, self.on_button_clicked, self._label_for_button)

        navigation_label = Gtk.Label("\n\nNavigation buttons:\n")
        first_grid.attach(navigation_label, 0, 4, 1, 1)

        helper.create_pos_group(first_grid, 5, 'Warp Dock Loot', warp_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(first_grid, 6, 'Align', align_target_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(first_grid, 7, 'Lock Target', lock_target_pos, self.on_button_clicked, self._label_for_button)

        navigation_label = Gtk.Label("\n\nGUI buttons:\n")
        first_grid.attach(navigation_label, 0, 8, 1, 1)

        helper.create_pos_group(first_grid, 9, 'Anomaly', warp_bar_pos, self.on_button_clicked, self._label_for_button)

        init_label = Gtk.Label("\n\nInit:\n")
        first_grid.attach(init_label, 0, 10, 1, 1)
        helper.create_pos_group(first_grid, 11, 'Eve Window', active_eve_pos, self.on_button_clicked, self._label_for_button)

        empty_label = Gtk.Label("\n\n\n\n\n\n\n")
        run_anomaly_game = Gtk.Button(label='Run Anomaly Game')
        run_anomaly_game.connect("clicked", self.on_button_run_anomaly)

        first_grid.attach(empty_label, 0, 12, 1, 1)
        first_grid.attach(run_anomaly_game, 0, 13, 1, 1)

        run_agent_game = Gtk.Button(label='Run Agent Game')
        run_agent_game.connect("clicked", self.on_button_run_agent)
        first_grid.attach(run_agent_game, 0, 14, 1, 1)

        run_travel_game = Gtk.Button(label='Run Travel Game')
        run_travel_game.connect("clicked", self.on_button_run_travel)
        first_grid.attach(run_travel_game, 0, 15, 1, 1)

        run_expediotion_game = Gtk.Button(label='Run Expedition Game')
        run_expediotion_game.connect("clicked", self.on_button_run_ded)
        first_grid.attach(run_expediotion_game, 0, 16, 1, 1)

        run_mission_game = Gtk.Button(label='Run Missions Game')
        run_mission_game.connect("clicked", self.on_button_run_missions)
        first_grid.attach(run_mission_game, 0, 17, 1, 1)

        bar_pos_label = Gtk.Label("GUI Positions:\n")
        second_grid.add(bar_pos_label)

        helper.create_pos_group(second_grid, 1, 'Item Bar End Y', item_bar_end_y, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 2, 'Anomaly End Y', anomaly_list_end_y, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 3, 'Anomaly Warp X', anomaly_warp_x, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 4, 'Travel Title', travel_title_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 5, 'Bar Item', bar_item_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 6, 'Drone In Bay', drone_in_bay_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 7, 'Anomaly info Close', anomaly_info_close_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 8, 'Copy Target Data', copy_target_data_pos, self.on_button_clicked, self._label_for_button)

        inventory_label = Gtk.Label("\n\nInventory Buttons:\n")
        second_grid.attach(inventory_label, 0, 9, 1, 1)

        helper.create_pos_group(second_grid, 10, 'Close Inventory', close_inventory_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 11, 'Loot All', loot_all_pos, self.on_button_clicked, self._label_for_button)

        inventory_label = Gtk.Label("\n\nShip Buttons:\n")
        second_grid.attach(inventory_label, 0, 12, 1, 1)

        helper.create_pos_group(second_grid, 13, 'Attack Module', attack_module_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 14, 'Speed Module', speed_module_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 15, 'Sub-Module 1', sub_modules_pos_1, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 16, 'Sub-Module 2', sub_modules_pos_2, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(second_grid, 17, 'Sub-Module 3', sub_modules_pos_3, self.on_button_clicked, self._label_for_button)

        bar_pos_label = Gtk.Label("\n")
        third_grid.add(bar_pos_label)

        helper.create_pos_group(third_grid, 1, 'Journal Button', journal_button_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 2, 'Journal Close Button', journal_close_button_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 3, 'Journal Expedition', journal_expeditions_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 4, 'Expedition Item', expeditions_item_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 5, 'Expedition List End Y', expeditions_list_end, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 6, 'End Travel Title', end_travel_title_pos, self.on_button_clicked, self._label_for_button)

        bar_pos_label = Gtk.Label("\n")
        third_grid.attach(bar_pos_label, 0, 7, 1, 1)

        helper.create_pos_group(third_grid, 8, 'Gate Bar', gate_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 9, 'Struct Bar', struct_bar_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 10, 'Grid Bar', grid_bar_pos, self.on_button_clicked, self._label_for_button)

        missions_label = Gtk.Label("\nMissions Possiotions:\n")
        third_grid.attach(missions_label, 0, 11, 1, 1)

        helper.create_pos_group(third_grid, 12, 'Agent Start Conversation', agent_start_conversation_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 13, 'Accept Mission', accept_mission_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 14, 'Mission Title', mission_title_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 15, 'Close Mission', close_mission_pos, self.on_button_clicked, self._label_for_button)
        helper.create_pos_group(third_grid, 16, 'Mission Path', mission_path_pos, self.on_button_clicked, self._label_for_button)

        helper.create_pos_group(third_grid, 17, 'Undock', undock_pos, self.on_button_clicked, self._label_for_button)

        self.mouseThread = MouseThread(self, self.x_pos_label, self.y_pos_label)
        self.mouseThread.start()

        self.move(100, 100)

    def on_button_run_missions(self, widget):
        pass

    def on_button_run_anomaly(self, widget):
        action.active_eve()

        warp = WarpToAnomaly()
        warp.start()
        #fixme add fuctionality to add path when path ends
        while not warp.is_anomaly_end():
            if not warp.is_anomaly_closed():
                kill = KillEnemy()
                kill.start()

                if kill.is_killed_rare_ship():
                    loot_wreck = LootWreck()
                    loot_wreck.start()
                else:
                    sleep(5)

            warp.start()

        travel = Travel()
        travel.set_iter_jump()
        while not travel.is_path_end():
            travel.start()

            warp = WarpToAnomaly()
            warp.start()
            while not warp.is_anomaly_end():
                if not warp.is_anomaly_closed():
                    kill = KillEnemy()
                    kill.start()

                    if kill.is_killed_rare_ship():
                        loot_wreck = LootWreck()
                        loot_wreck.start()
                    else:
                        sleep(5)

                warp.start()

    def on_button_run_agent(self, widget):
        pass

    def on_button_run_travel(self, widget):
        action.active_eve()

        travel = Travel()
        travel.start()

    def on_button_run_ded(self, widget):
        action.active_eve()

        expedition_pos, expedition_info = action.set_expedition_destination()
        #s = "16 hours, 48 minutes and 50 seconds	2018.01.29 12:50:00	Grinacanne	0	Serpentis Narcotic Warehouses"
        #expedition_info = action.parse_expedition_data(s)
        #expedition_pos = expeditions_item_pos
        #expedition_pos[1] = expedition_pos[1] + 20

        while expedition_info is not None:
            self.on_button_run_anomaly(widget)

            action.warp_to_ded_complex(expedition_pos)

            ded_complex = ded_complex_factory.create_complex(expedition_info['name'])
            ded_complex.start()

            expedition_pos, expedition_info = action.set_expedition_destination()

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
