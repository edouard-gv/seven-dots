import threading
from statemachine import StateMachine, State


class DotsMachine(StateMachine):
    # States
    blank_screen = State(initial=True)
    hello = State()
    bye = State()
    countdown = State()

    open_palm = (
        blank_screen.to(hello)
        | bye.to(hello)
        | countdown.to(hello)
        | hello.to(hello, internal=True)
    )
    closed_fist = (
        blank_screen.to(bye)
        | hello.to(bye)
        | countdown.to(bye)
        | bye.to(bye, internal=True)
    )
    turn_off = bye.to(blank_screen)
    victory = (
        blank_screen.to(countdown)
        | hello.to(countdown)
        | bye.to(countdown)
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
        super(DotsMachine, self).__init__(*args, **kwargs)

    def on_enter_bye(self, event, state):
        self.turn_off_timer = self.get_timer(2, self.turn_off)
        self.turn_off_timer.start()

    def on_enter_countdown(self, event, state):
        self.countdown_value = 120 # 120 ticks are 2 minutes
        if self.countdown_timer is not None:
            self.countdown_timer.cancel()
        self.countdown_timer = self.get_timer(1, self.countdown_tick)
        self.countdown_timer.start()

    def countdown_tick(self):
        self.controler.post_process()
        if self.countdown_value > 0:
            self.countdown_value -= 1
            self.countdown_timer = self.get_timer(1, self.countdown_tick)
            self.countdown_timer.start()
        else:
            self.closed_fist()

    def on_enter_state(self, event, state):
        if self.turn_off_timer is not None:
            self.turn_off_timer.cancel()
            self.turn_off_timer = None
        self.nb_transitions += 1
        print(f"On '{event}', on the '{state.id}' state.")
        # at initialization of the machine, the controler doesn't have the machine yet,
        # but the machine enters the initial state and triggers the enter state event
        if hasattr(self.controler, "machine") and state != self.countdown:
            self.controler.post_process()


if __name__ == "__main__":
    m = DotsMachine(None)
    m._graph().write_png("dots_machine.png")
