import json
import time

from werkzeug.exceptions import BadRequest, NotFound
from json.decoder import JSONDecodeError

STATE_SEQ = 0

class Database:
    def __init__(self):
        self.submarine = {"x": 0, "y": 0}
        self.artifact = {}
        self.fishes = []
        self.last_fish_index = 0
        self.state_file = None
        self.init_submarine()

    def init_submarine(self):
        while True:
            try:
                with open("state-init.json", "r") as state_ro:
                    state = json.load(state_ro)
                    submarine_state = state["submarine"]

                    self.submarine = {"x": submarine_state["x"], "y": submarine_state["y"]}
                    print("Init the submarine: ", self.submarine)
                    return

            except (JSONDecodeError, FileNotFoundError):
                time.sleep(2)
                print("Init state file not present yet...waiting for display module!")

    def get_submarine(self):
        return self.submarine

    def move_submarine(self, payload):
        if payload is None:
            raise BadRequest("Bad request")

        if "x" not in payload and "y" not in payload:
            raise BadRequest("Bad request")

        if "x" in payload:
            self.submarine["x"] += payload["x"]

        if "y" in payload:
            self.submarine["y"] += payload["y"]

        print("Updated submarine: ", self.submarine)

    def get_fishes(self):
        return self.fishes

    def add_fish(self, payload):
        if payload is None:
            raise BadRequest("Bad request")

        if "x" not in payload or "y" not in payload:
            raise BadRequest("Bad request")
        else:
            x = payload["x"]
            y = payload["y"]

            self.fishes.insert(self.last_fish_index, {"x": x, "y": y})
            self.last_fish_index = (self.last_fish_index + 1) % 5

            if len(self.fishes) > 5:
                self.fishes = self.fishes[0:5]

            print("Last fish index: ", self.last_fish_index)
            print("Fishes: ", self.fishes)

    def get_artifact(self):
        return self.artifact

    def update_artifact(self, payload):
        if payload is None:
            raise BadRequest("Bad request")

        if "x" not in payload and "y" not in payload:
            self.artifact = {}
        else:
            x = payload["x"]
            y = payload["y"]
            self.artifact = {"x": x, "y": y}

        print("New artifact: ", self.artifact)

    def flush_state(self):
        global STATE_SEQ

        state = {
            "submarine": self.submarine,
            "fishes": self.fishes,
            "artifact": self.artifact
        }

        with open("state-" + str(STATE_SEQ) +  ".json", "w") as state_file:
            json_object = json.dumps(state, indent = 4)
            state_file.write(json_object)

            STATE_SEQ += 1