import display_utils.countdown
from display_utils import alphabet
from dots_machine import DotsMachine


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


def compute_display(machine: DotsMachine):
    display = initialize_display()
    if machine.current_state == machine.hello:
        alphabet.writeCenter("Salut", display)
    if machine.current_state == machine.bye:
        alphabet.writeCenter("Bye", display)
    if machine.current_state == machine.blank_screen:
        clear_display(display)
    if machine.current_state == machine.black_screen:
        fill_display(display)
    if machine.current_state == machine.countdown_confirm_stop:
        alphabet.writeCenter("Stop ?", display)
    if machine.current_state == machine.menu_system:
        alphabet.write("1 Off", display)
        alphabet.write("2 MAJ", display, line_shift=1)
    if machine.current_state == machine.shutdown_confirm:
        alphabet.writeCenter("OFF ?", display)
    if machine.current_state == machine.update_confirm:
        alphabet.writeCenter("MAJ ?", display)
    if machine.current_state == machine.system_shutdown:
        alphabet.writeCenter("...", display)
    if machine.current_state == machine.system_update:
        alphabet.writeCenter("...", display)

    if machine.current_state == machine.countdown:
        if machine.countdown_running():
            display_utils.countdown.lit_all_positions_for_seconds(machine.countdown_value, display)
            if machine.show_countdown():
                alphabet.write(
                    display_utils.countdown.print_seconds(machine.countdown_value), display
                )
    else:
        if machine.countdown_running() and not machine.current_state == machine.bye:
            alphabet.write(
                display_utils.countdown.print_seconds(machine.countdown_value), display
            )
    return display
