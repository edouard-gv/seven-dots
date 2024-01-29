import threading
from statemachine import StateMachine, State


class DotsMachine(StateMachine):
    # States
    blank_screen = State(initial=True)
    hello = State()
    bye = State()
    countdown = State()
    countdown_confirm_stop = State()

    open_palm = (
        blank_screen.to(hello)
        | bye.to(hello)
        | countdown.to(hello)
        | hello.to(hello, internal=True)
    )
    closed_fist = (
        blank_screen.to(bye)
        | hello.to(bye, unless="countdown_running")
        | hello.to(countdown_confirm_stop, cond="countdown_running")
        | countdown.to(countdown_confirm_stop)
        | bye.to(bye, internal=True)
        | countdown_confirm_stop.to(countdown_confirm_stop, internal=True)
    )
    turn_off = bye.to(blank_screen) | countdown_confirm_stop.to(bye) | countdown.to(bye)

    victory = (
        blank_screen.to(countdown, on="set_countdown_to_120")
        | hello.to(countdown, on="set_countdown_to_120")
        | bye.to(countdown, on="set_countdown_to_120")
        | countdown.to(countdown, on="set_countdown_to_120", unless="action_was_victory")
        | countdown.to(countdown, cond="action_was_victory", internal=True)
    )

    pointing_up = (
        blank_screen.to(countdown, on="set_countdown_to_60")
        | hello.to(countdown, on="set_countdown_to_60")
        | bye.to(countdown, on="set_countdown_to_60")
        | countdown.to(countdown, on="set_countdown_to_60", unless="action_was_pointing_up")
        | countdown.to(countdown, cond="action_was_pointing_up", internal=True)
    )

    none = (
        countdown.to(countdown, unless="action_was_none")
        | countdown.to(countdown, cond="action_was_none", internal=True)
    )

    thumb_up = countdown_confirm_stop.to(bye) | bye.to(bye, internal=True)

    thumb_down = (
        countdown_confirm_stop.to(countdown) 
        | countdown.to(countdown, internal=True)
    )

    # timer factory that can be overiden for testing
    def get_timer(nb_ticks, callback):
        return threading.Timer(nb_ticks, callback)

    def __init__(self, controler, get_timer=get_timer, *args, **kwargs):
        self.turn_off_timer = None
        self.nb_transitions = 0
        self.controler = controler
        self.countdown_value = 0
        self.countdown_timer = None
        self.get_timer = get_timer
        self.previous_action = None
        super(DotsMachine, self).__init__(*args, **kwargs)

    def on_enter_bye(self, event, state):
        self.turn_off_timer = self.get_timer(2, self.turn_off)
        if self.countdown_running():
            self.countdown_timer.cancel()
            self.countdown_timer = None
        self.turn_off_timer.start()

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

    def action_was_none(self, event, state):
        return self.previous_action == 'none'

    def on_enter_countdown(self, event, state):
        if not self.countdown_running():
            self.countdown_timer = self.get_timer(1, self.countdown_tick)
            self.countdown_timer.start()

    def countdown_tick(self):
        if self.countdown_value > 0:
            self.countdown_value -= 1
            self.countdown_timer = self.get_timer(1, self.countdown_tick)
            self.countdown_timer.start()
        else:
            if self.current_state in [self.countdown, self.countdown_confirm_stop]:
                self.turn_off()
        self.controler.post_process()

    def on_enter_state(self, event, state):
        self.previous_action = event
        if self.turn_off_timer is not None:
            self.turn_off_timer.cancel()
            self.turn_off_timer = None
        self.nb_transitions += 1
        #print(f"On '{event}', on the '{state.id}' state.")
        # at initialization of the machine, the controler doesn't have the machine yet,
        # but the machine enters the initial state and triggers the enter state event
        if hasattr(self.controler, "machine") and state != self.countdown:
            self.controler.post_process()

    def countdown_running(self):
        return self.countdown_timer is not None and self.countdown_timer.is_alive()


if __name__ == "__main__":
    m = DotsMachine(None)
    m._graph().write_png("dots_machine.png")
