import threading

from statemachine import StateMachine, State


class DotsMachine(StateMachine):
    # States
    black_screen = State(initial=True)
    blank_screen = State()
    hello = State()
    bye = State()
    countdown = State()
    countdown_confirm_stop = State()
    menu_system = State()
    shutdown_confirm = State()
    update_confirm = State()
    system_shutdown = State(final=True)
    system_update = State(final=True)

    init = (black_screen.to(blank_screen))

    open_palm = (
            blank_screen.to(hello)
            | bye.to(hello)
            | countdown.to(countdown_confirm_stop, unless="action_was_open_palm")
            | countdown.to(countdown, cond="action_was_open_palm", internal=True)
            | hello.to(hello, internal=True)
            | shutdown_confirm.to(menu_system)
            | update_confirm.to(menu_system)
            | menu_system.to(blank_screen, unless="action_was_open_palm")
            | menu_system.to(menu_system, cond="action_was_open_palm", internal=True)
            | countdown_confirm_stop.to(countdown, unless="action_was_open_palm")
            | countdown_confirm_stop.to(countdown_confirm_stop, cond="action_was_open_palm", internal=True)
    )
    closed_fist = (
            hello.to(bye)
            | countdown.to(countdown, unless="action_was_closed_fist")
            | countdown.to(countdown, cond="action_was_closed_fist", internal=True)
    )
    turn_off = bye.to(blank_screen) | countdown_confirm_stop.to(bye) | countdown.to(bye)

    victory = (
            blank_screen.to(countdown, on="set_countdown_to_120")
            | hello.to(countdown, on="set_countdown_to_120")
            | bye.to(countdown, on="set_countdown_to_120")
            | countdown.to(countdown, on="set_countdown_to_120", unless="action_was_victory")
            | countdown.to(countdown, cond="action_was_victory", internal=True)
            | menu_system.to(update_confirm)
    )

    pointing_up = (
            blank_screen.to(countdown, on="set_countdown_to_60")
            | hello.to(countdown, on="set_countdown_to_60")
            | bye.to(countdown, on="set_countdown_to_60")
            | countdown.to(countdown, on="set_countdown_to_60", unless="action_was_pointing_up")
            | countdown.to(countdown, cond="action_was_pointing_up", internal=True)
            | menu_system.to(shutdown_confirm)
    )

    none = (
            countdown.to(countdown, unless="action_was_none")
            | countdown.to(countdown, cond="action_was_none", internal=True)
            | menu_system.to(menu_system, unless="action_was_none")
            | menu_system.to(menu_system, cond="action_was_none", internal=True)
            | countdown_confirm_stop.to(countdown_confirm_stop, unless="action_was_none")
            | countdown_confirm_stop.to(countdown_confirm_stop, cond="action_was_none", internal=True)
    )

    thumb_up = (
            countdown_confirm_stop.to(bye)
            | shutdown_confirm.to(system_shutdown)
            | update_confirm.to(system_update)
    )

    iloveyou = (blank_screen.to(menu_system))

    def is_system_state(self):
        return self.current_state.value.lower().startswith("system_")

    # timer factory that can be overiden for testing
    def get_timer(nb_ticks, callback):
        return threading.Timer(nb_ticks, callback)

    def __init__(self, controller, get_timer=get_timer, *args, **kwargs):
        self.turn_off_timer = None
        self.nb_transitions = 0
        self.controller = controller
        self.countdown_value = 0
        self.countdown_timer = None
        self.get_timer = get_timer
        self.previous_action = None
        self.slow_pace = False
        super(DotsMachine, self).__init__(*args, **kwargs)

    def on_enter_bye(self, event, state):
        self.turn_off_timer = self.get_timer(2, self.turn_off)
        if self.countdown_running():
            if self.countdown_timer is not None:
                self.countdown_timer.cancel()
                self.countdown_timer = None
        self.turn_off_timer.start()

    def on_enter_blank_screen(self, event, state):
        self.slow_pace = True

    def on_exit_blank_screen(self, event, state):
        self.slow_pace = False

    def set_countdown_to_120(self):
        if not self.countdown_running():
            self.countdown_value = 120  # 120 ticks are 2 minutes
        else:
            self.countdown_value += 120

    def set_countdown_to_60(self):
        if not self.countdown_running():
            self.countdown_value = 60  # 60 ticks are 1 minute
        else:
            self.countdown_value += 60

    def action_was_pointing_up(self, event, state):
        return self.previous_action == 'pointing_up'

    def action_was_victory(self, event, state):
        return self.previous_action == 'victory'

    def action_was_open_palm(self, event, state):
        return self.previous_action == 'open_palm'

    def action_was_none(self, event, state):
        return self.previous_action == 'none'

    def action_was_closed_fist(self, event, state):
        return self.previous_action == 'closed_fist'

    def on_enter_countdown(self, event, state):
        if not self.countdown_running():
            self.countdown_timer = self.get_timer(1, self.countdown_tick)
            self.countdown_timer.start()
        # I don't understand why I have to force the refresh, on_enter_state should do it (cf issue #16)
        self.controller.process_state()

    def countdown_tick(self):
        if self.countdown_value > 0:
            self.countdown_value -= 1
            self.countdown_timer = self.get_timer(1, self.countdown_tick)
            self.countdown_timer.start()
        else:
            if self.current_state in [self.countdown, self.countdown_confirm_stop]:
                self.turn_off()
            if self.countdown_timer is not None:
                self.countdown_timer.cancel()
                self.countdown_timer = None
        self.controller.process_state()

    def on_enter_state(self, event, state):
        if state in self.final_states:
            self.slow_pace = True
        self.previous_action = event
        if self.turn_off_timer is not None:
            self.turn_off_timer.cancel()
            self.turn_off_timer = None
        self.nb_transitions += 1
        # print(f"On '{event}', on the '{state.id}' state.")
        # at initialization of the machine, the controller doesn't have the machine yet,
        # but the machine enters the initial state and triggers the enter state event
        if hasattr(self.controller, "machine") and self.controller.machine is not None:  # and state != self.countdown:
            self.controller.process_state()

    def countdown_running(self):
        return self.countdown_timer is not None and self.countdown_timer.is_alive()


if __name__ == "__main__":
    m = DotsMachine(None)
    m._graph().write_png("doc/dots_machine.png")
