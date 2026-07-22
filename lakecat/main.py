import curses
import time

DOOR = [
    " ______",
    "|      |",
    "| _    |",
    "|      |",
    "|______|",
]
DOOR_WIDTH = max(len(line) for line in DOOR)
DOOR_HEIGHT = len(DOOR)


def run():
    curses.wrapper(main)


def draw_door(stdscr, door_x, door_y, height, width):
    for i, line in enumerate(DOOR):
        row = door_y + i
        if row >= height:
            break
        max_len = width - door_x
        if max_len <= 0:
            break
        stdscr.addstr(row, door_x, line[:max_len])


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

        door_y = max(1, (height - DOOR_HEIGHT) // 2)
        door_bottom = door_y + DOOR_HEIGHT - 1
        door_x = max(0, width - DOOR_WIDTH)

        if scene == "home":
            touching_door = door_y <= y <= door_bottom and x < DOOR_WIDTH
            if touching_door:
                scene = "town"
                x = max(0, door_x - 2)
                y = door_y + DOOR_HEIGHT // 2
        elif scene == "town":
            touching_door = door_y <= y <= door_bottom and x >= door_x
            if touching_door:
                scene = "home"
                x = DOOR_WIDTH
                y = door_y + DOOR_HEIGHT // 2

        stdscr.clear()

        title = "<Town>" if scene == "town" else "<Home>"
        title_x = max(0, (width - len(title)) // 2)
        stdscr.addstr(0, title_x, title)

        if scene == "home":
            draw_door(stdscr, 0, door_y, height, width)
        else:
            draw_door(stdscr, door_x, door_y, height, width)

        stdscr.addstr(y, x, "🐈")
        stdscr.refresh()

        time.sleep(1 / 60)
