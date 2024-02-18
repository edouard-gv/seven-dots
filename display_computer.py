import alphabet


def initialize_display():
    display = [[0b0000000 for _ in range(7)] for _ in range(4)]
    return display


def fill_display(display):
    for i in range(4):
        for j in range(7):
            display[i][j] = 0b1111111


def clear_display(display):
    for i in range(4):
        for j in range(7):
            display[i][j] = 0b0000000


def compute_display(machine):
    display = initialize_display()
    if machine.current_state.name == "Hello":
        alphabet.writeCenter("Salut", display)
    if machine.current_state.name == "Bye":
        alphabet.writeCenter("Bye", display)
    if machine.current_state.name == "Blank screen":
        clear_display(display)
    if machine.current_state.name == "Black screen":
        fill_display(display)
    if machine.current_state.name == "Countdown confirm stop":
        alphabet.writeCenter("Stop ?", display)
    if machine.current_state.name == "Countdown":
        if machine.countdown_running():
            alphabet.writeCenter(
                alphabet.print_seconds(machine.countdown_value), display
            )
    else:
        if machine.countdown_running() and not machine.current_state.name == "Bye":
            alphabet.write(
                alphabet.print_seconds(machine.countdown_value), display, line_shift=3
            )
    return display
