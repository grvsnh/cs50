import curses
import random
import time


# ==========================================================
# Entry
# ==========================================================


def main():
    curses.wrapper(app)


def app(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.start_color()
    init_colors()
    menu(stdscr)


# ==========================================================
# Colors
# ==========================================================


def init_colors():
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # normal
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # X
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)  # O
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # cursor
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  # title
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)  # win
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # info


# ==========================================================
# Safe drawing helpers
# ==========================================================


def safe_addstr(stdscr, y, x, text, color=0, attr=0):
    h, w = stdscr.getmaxyx()
    if y < 0 or y >= h:
        return
    if x < 0:
        x = 0
    if x >= w:
        return
    if x + len(text) >= w:
        text = text[: max(0, w - x - 1)]
    try:
        if color:
            stdscr.attron(curses.color_pair(color))
        if attr:
            stdscr.attron(attr)
        stdscr.addstr(y, x, text)
        if attr:
            stdscr.attroff(attr)
        if color:
            stdscr.attroff(curses.color_pair(color))
    except curses.error:
        pass


def cx(stdscr, text):
    _, w = stdscr.getmaxyx()
    return max(0, w // 2 - len(text) // 2)


def cy(stdscr, offset=0):
    h, _ = stdscr.getmaxyx()
    return h // 2 + offset


def draw_center(stdscr, y, text, color=0, attr=0):
    safe_addstr(stdscr, y, cx(stdscr, text), text, color, attr)


# ==========================================================
# ASCII TITLE
# ==========================================================

ASCII_TITLE = [
    "████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗     ",
    "╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║     ",
    "   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║     ",
    "   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║     ",
    "   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗",
    "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝",
    "              ██████╗  █████╗ ███╗   ███╗███████╗███████╗",
    "             ██╔════╝ ██╔══██╗████╗ ████║██╔════╝██╔════╝",
    "             ██║  ███╗███████║██╔████╔██║█████╗  ███████╗",
    "             ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ╚════██║",
    "             ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗███████║",
    "              ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝",
]


def animate_ascii_title(stdscr, start_y):
    for i, line in enumerate(ASCII_TITLE):
        draw_center(stdscr, start_y + i, line, 5)
        stdscr.refresh()
        time.sleep(0.03)


# ==========================================================
# Main Menu
# ==========================================================

MENU = ["Tic Tac Toe", "Rock Paper Scissors", "Number Guessing Game", "Exit"]


def menu(stdscr):
    idx = 0
    animated = False

    while True:
        stdscr.clear()

        title_start_y = cy(stdscr, -10)

        if not animated:
            animate_ascii_title(stdscr, title_start_y)
            animated = True
        else:
            for i, line in enumerate(ASCII_TITLE):
                draw_center(stdscr, title_start_y + i, line, 5)

        for i, item in enumerate(MENU):
            draw_center(stdscr, cy(stdscr, 4 + i), item, 4 if i == idx else 0)

        draw_center(stdscr, cy(stdscr, 9), "↑ ↓ Move   Enter Select   Q Quit", 7)
        stdscr.refresh()

        k = stdscr.getch()
        if k == curses.KEY_UP:
            idx = (idx - 1) % len(MENU)
        elif k == curses.KEY_DOWN:
            idx = (idx + 1) % len(MENU)
        elif k in [10, 13]:
            if idx == 0:
                ttt_menu(stdscr)
            elif idx == 1:
                rps(stdscr)
            elif idx == 2:
                number_guess(stdscr)
            else:
                return
        elif k in [ord("q"), ord("Q")]:
            return


# ==========================================================
# Tic Tac Toe Menu
# ==========================================================


def ttt_menu(stdscr):
    options = ["Play vs Computer", "Play vs Friend", "Back"]
    idx = 0

    while True:
        stdscr.clear()
        draw_center(stdscr, cy(stdscr, -4), "TIC TAC TOE", 5, curses.A_BOLD)

        for i, opt in enumerate(options):
            draw_center(stdscr, cy(stdscr, -1 + i), opt, 4 if i == idx else 0)

        draw_center(stdscr, cy(stdscr, 4), "↑ ↓ Move   Enter Select   Q Back", 7)
        stdscr.refresh()

        k = stdscr.getch()
        if k == curses.KEY_UP:
            idx = (idx - 1) % len(options)
        elif k == curses.KEY_DOWN:
            idx = (idx + 1) % len(options)
        elif k in [10, 13]:
            if idx == 0:
                tic_tac_toe(stdscr, vs_ai=True)
            elif idx == 1:
                tic_tac_toe(stdscr, vs_ai=False)
            else:
                return
        elif k in [ord("q"), ord("Q")]:
            return


# ==========================================================
# Tic Tac Toe Logic + UI (unchanged)
# ==========================================================


def ttt_winner(board, player):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    return any(all(board[i] == player for i in w) for w in wins)


def ttt_ai_move(board):
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if ttt_winner(board, "O"):
                board[i] = " "
                return i
            board[i] = " "
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if ttt_winner(board, "X"):
                board[i] = " "
                return i
            board[i] = " "
    return random.choice([i for i in range(9) if board[i] == " "])


def tic_tac_toe(stdscr, vs_ai):
    board = [" "] * 9
    cursor = 0
    player = "X"

    while True:
        stdscr.clear()
        draw_center(stdscr, cy(stdscr, -6), "TIC TAC TOE", 5, curses.A_BOLD)
        draw_ttt_board(stdscr, board, cursor)
        draw_center(stdscr, cy(stdscr, 6), "Arrows Move   Enter Place   Q Quit", 7)
        stdscr.refresh()

        if ttt_winner(board, "X"):
            return end_screen(stdscr, "X WINS!", 6)
        if ttt_winner(board, "O"):
            return end_screen(stdscr, "O WINS!", 6)
        if " " not in board:
            return end_screen(stdscr, "DRAW!", 7)

        if vs_ai and player == "O":
            ai_think(stdscr)
            board[ttt_ai_move(board)] = "O"
            player = "X"
            continue

        k = stdscr.getch()
        if k == curses.KEY_LEFT:
            cursor = (cursor - 1) % 9
        elif k == curses.KEY_RIGHT:
            cursor = (cursor + 1) % 9
        elif k == curses.KEY_UP:
            cursor = (cursor - 3) % 9
        elif k == curses.KEY_DOWN:
            cursor = (cursor + 3) % 9
        elif k in [10, 13] and board[cursor] == " ":
            board[cursor] = player
            player = "O" if player == "X" else "X"
        elif k in [ord("q"), ord("Q")]:
            return


def draw_ttt_board(stdscr, board, cursor):
    h, w = stdscr.getmaxyx()
    sy = h // 2 - 4
    sx = w // 2 - 8

    grid = [
        "┌───┬───┬───┐",
        "│   │   │   │",
        "├───┼───┼───┤",
        "│   │   │   │",
        "├───┼───┼───┤",
        "│   │   │   │",
        "└───┴───┴───┘",
    ]

    for i, line in enumerate(grid):
        safe_addstr(stdscr, sy + i, sx, line, 1)

    for i in range(9):
        r, c = divmod(i, 3)
        y = sy + 1 + r * 2
        x = sx + 2 + c * 4

        if i == cursor:
            stdscr.attron(curses.color_pair(4))

        if board[i] == "X":
            safe_addstr(stdscr, y, x, "X", 2)
        elif board[i] == "O":
            safe_addstr(stdscr, y, x, "O", 3)
        else:
            safe_addstr(stdscr, y, x, " ")

        if i == cursor:
            stdscr.attroff(curses.color_pair(4))


def ai_think(stdscr):
    for dots in ["AI thinking.", "AI thinking..", "AI thinking..."]:
        draw_center(stdscr, cy(stdscr, 4), dots, 7)
        stdscr.refresh()
        time.sleep(0.3)


# ==========================================================
# Rock Paper Scissors (unchanged)
# ==========================================================


def rps_result(player, cpu):
    if player == cpu:
        return "Draw"
    if (
        (player == "Rock" and cpu == "Scissors")
        or (player == "Paper" and cpu == "Rock")
        or (player == "Scissors" and cpu == "Paper")
    ):
        return "You Win"
    return "You Lose"


def rps(stdscr):
    options = ["Rock", "Paper", "Scissors"]
    idx = 0

    while True:
        stdscr.clear()
        draw_center(stdscr, cy(stdscr, -4), "ROCK PAPER SCISSORS", 5, curses.A_BOLD)

        for i, o in enumerate(options):
            draw_center(stdscr, cy(stdscr, -1 + i), o, 4 if i == idx else 0)

        stdscr.refresh()
        k = stdscr.getch()

        if k == curses.KEY_UP:
            idx = (idx - 1) % 3
        elif k == curses.KEY_DOWN:
            idx = (idx + 1) % 3
        elif k in [10, 13]:
            player = options[idx]
            for dots in ["AI choosing.", "AI choosing..", "AI choosing..."]:
                draw_center(stdscr, cy(stdscr, 4), dots, 7)
                stdscr.refresh()
                time.sleep(0.3)
            cpu = random.choice(options)
            result = rps_result(player, cpu)
            stdscr.clear()
            draw_center(stdscr, cy(stdscr, -1), f"You: {player}")
            draw_center(stdscr, cy(stdscr, 1), f"AI: {cpu}")
            draw_center(stdscr, cy(stdscr, 3), result, 6 if result == "You Win" else 7)
            draw_center(stdscr, cy(stdscr, 5), "Press any key", 7)
            stdscr.refresh()
            stdscr.getch()
            return
        elif k in [ord("q"), ord("Q")]:
            return


# ==========================================================
# Number Guessing Game (unchanged)
# ==========================================================


def number_guess(stdscr):
    secret = random.randint(1, 100)
    attempts = 0

    while True:
        stdscr.clear()
        draw_center(stdscr, cy(stdscr, -2), "NUMBER GUESSING GAME", 5, curses.A_BOLD)
        draw_center(stdscr, cy(stdscr), f"Attempts: {attempts}")
        draw_center(stdscr, cy(stdscr, 2), "Enter number (1–100) or Q")
        stdscr.refresh()

        curses.echo()
        guess = stdscr.getstr(cy(stdscr, 3), cx(stdscr, "000"), 5).decode()
        curses.noecho()

        if guess.lower() == "q":
            return
        if not guess.isdigit():
            continue

        attempts += 1
        g = int(guess)

        if g == secret:
            stdscr.clear()
            draw_center(stdscr, cy(stdscr), "CORRECT!", 6, curses.A_BOLD)
            draw_center(stdscr, cy(stdscr, 2), f"In {attempts} attempts")
            draw_center(stdscr, cy(stdscr, 4), "Press any key")
            stdscr.refresh()
            stdscr.getch()
            return

        draw_center(stdscr, cy(stdscr, 5), "Too Low!" if g < secret else "Too High!", 7)
        stdscr.refresh()
        time.sleep(0.5)


# ==========================================================
# End Screen
# ==========================================================


def end_screen(stdscr, msg, color):
    stdscr.clear()
    draw_center(stdscr, cy(stdscr), msg, color, curses.A_BOLD)
    draw_center(stdscr, cy(stdscr, 2), "Press any key", 7)
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    main()
