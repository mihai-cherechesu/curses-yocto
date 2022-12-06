import curses
import json
import os
import time

from json.decoder import JSONDecodeError
from curses import wrapper, curs_set, init_pair

submarine_model = [
    "                     _",
    "                    | \|",
    "                     '.|",
    "     _-   _-    _-  _-||    _-    _-  _-   _-    _-    _-",
    "       _-    _-   - __||___    _-       _-    _-    _-",
    "    _-   _-    _-  |   _   |       _-   _-    _-",
    "      _-    _-    /_) (_) (_\        _-    _-       _-",
    "              _.-'           `-._      ________       _-",
    "        _..--`                   `-..'       .'",
    "    _.-'  o/o                     o/o`-..__.'        ~  ~",
    " .-'      o|o                     o|o      `.._.  // ~  ~",
    " `-._     o|o                     o|o        |||<|||~  ~",
    "     `-.__o\o                     o|o       .'-'  \\ ~  ~",
    "          `-.______________________\_...-``'.       ~  ~",
    "                                    `._______`.",
]

fish_model = [
    "|\   \\\\__     o",
    "| \_/    o \    o ",
    "> _   (( <_  oo  ",
    "| / \__+___/      ",
    "|/     |/",
]

artifact_model = [
    "  .     '     ,",
    "    _________",
    " _ /_|_____|_\ _",
    "   '. \   / .'",
    "     '.\ /.'",
    "       '.'"
]

HEIGHT = 0
WIDTH = 0
STATE_SEQ = -1
prev_state = {}

def draw_byte(stdscr, byte, x, y, attr):
    if x >= 0 and y >= 0 and x < WIDTH and y < HEIGHT:
        if byte != " ":
            stdscr.addstr(y, x, byte, attr)
        else:
            stdscr.addstr(y, x, byte, curses.A_NORMAL)

def draw_model(stdscr, x, y, model, attr):
    for line_idx in range(0, len(model)):
        for byte_idx in range(0, len(model[line_idx])):
            draw_byte(stdscr, model[line_idx][byte_idx], x + byte_idx, y + line_idx, attr)

def read_state():
    global STATE_SEQ

    if STATE_SEQ == -1:
        initial_state = {
            "submarine": {"x": WIDTH // 2, "y": HEIGHT // 2},
            "fishes": [],
            "artifact": {}
        }

        with open('state-init.json','w') as state_file:
            json_object = json.dumps(initial_state, indent = 4)
            state_file.write(json_object)

        STATE_SEQ = 0
        return initial_state

    else:
        try:
            with open('state-' + str(STATE_SEQ) + '.json', 'r') as state_file:
                state = json.load(state_file)

            os.remove('state-' + str(STATE_SEQ) + '.json')
            STATE_SEQ += 1
            return state

        except (FileNotFoundError, JSONDecodeError):
            return prev_state



def main(stdscr):
    global HEIGHT, WIDTH, prev_state

    curs_set(False)
    stdscr.clear()

    HEIGHT, WIDTH = stdscr.getmaxyx()

    curses.start_color()
    curses.use_default_colors()

    BKG_COL = 17

    curses.init_pair(1, BKG_COL, BKG_COL)
    curses.init_pair(2, 119, BKG_COL)
    curses.init_pair(3, 166, BKG_COL)
    curses.init_pair(4, 227, BKG_COL)

    stdscr.bkgd(' ', curses.color_pair(1))

    while True:

        state = read_state()

        if state != prev_state:
            stdscr.clear()
            prev_state = state
        else:
            continue

        submarine_x = state["submarine"]["x"]
        submarine_y = state["submarine"]["y"]

        draw_model(stdscr, submarine_x, submarine_y, submarine_model, curses.color_pair(2) | curses.A_BOLD)

        fishes = state["fishes"]
        for fish in fishes:
            fish_x = fish["x"]
            fish_y = fish["y"]

            draw_model(stdscr, fish_x, fish_y, fish_model, curses.color_pair(3) | curses.A_BOLD)


        artifact = state["artifact"]
        if artifact != {}:
            artifact_x = artifact["x"]
            artifact_y = artifact["y"]

            draw_model(stdscr, artifact_x, artifact_y, artifact_model, curses.color_pair(4) | curses.A_BOLD)

        stdscr.refresh()

wrapper(main)