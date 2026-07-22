import curses
import time

DOOR_LEFT = [
    " ______",
    "/      /",
    "/      /",
    "/  .   /",
    "/______/",
]
DOOR_RIGHT = [
    "______ ",
    "\\      \\",
    " \\      \\",
    "  \\   .  \\",
    "   \\______\\",
]
DOOR_WIDTH = max(len(line) for line in DOOR_LEFT)


def run():
    curses.wrapper(main)


def draw_door(stdscr, door, door_x, door_y, height):
    for i, line in enumerate(door):
        if door_y + i < height:
            stdscr.addstr(door_y + i, door_x, line)


def main(stdscr):
    curses.curs_set(0)      # 커서 숨기기
    stdscr.nodelay(True)    # 키가 없어도 계속 진행
    stdscr.keypad(True)     # 방향키 사용

    height, width = stdscr.getmaxyx()
    scene = "home"
    x = width // 2
    y = height // 2

    while True:
        key = stdscr.getch()
        height, width = stdscr.getmaxyx()

        if key == curses.KEY_UP:
            y -= 1
        elif key == curses.KEY_DOWN:
            y += 1
        elif key == curses.KEY_LEFT:
            x -= 2
        elif key == curses.KEY_RIGHT:
            x += 2
        elif key == ord("q"):
            break

        y = max(1, min(y, height - 1))
        x = max(0, min(x, width - 3))

        door_y = max(1, (height - len(DOOR_LEFT)) // 2)
        door_bottom = door_y + len(DOOR_LEFT) - 1

        door_x = max(0, width - DOOR_WIDTH - 1)

        if scene == "home":
            touching_door = door_y <= y <= door_bottom and x < DOOR_WIDTH
            if touching_door:
                scene = "town"
                x = width // 2
                y = height // 2
        elif scene == "town":
            touching_door = door_y <= y <= door_bottom and x >= door_x
            if touching_door:
                scene = "home"
                x = width // 2
                y = height // 2

        stdscr.clear()

        title = "<Town>" if scene == "town" else "<Home>"
        title_x = max(0, (width - len(title)) // 2)
        stdscr.addstr(0, title_x, title)

        if scene == "home":
            draw_door(stdscr, DOOR_LEFT, 0, door_y, height)
        else:
            draw_door(stdscr, DOOR_RIGHT, door_x, door_y, height)

        stdscr.addstr(y, x, "🐈")
        stdscr.refresh()

        time.sleep(1 / 60)
