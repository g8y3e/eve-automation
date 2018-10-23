import action

from process.travel import Travel


class MissionRun:
    def start(self):
        mission_name = action.get_mission_from_agent()
        action.undock()
        action.set_mission_destination()

        travel = Travel()
        travel.start()

        action.set_mission_destination()