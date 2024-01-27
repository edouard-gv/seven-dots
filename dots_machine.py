import threading
from statemachine import StateMachine, State


class DotsMachine(StateMachine):
    # States
    blank_screen = State(initial=True)
    hello = State()
    bye = State()

    open_palm = blank_screen.to(hello) | bye.to(hello) | hello.to(hello, internal=True)
    closed_fist = blank_screen.to(bye) | hello.to(bye) | bye.to(bye, internal=True)
    turn_off = bye.to(blank_screen)

    def __init__(self, controler, *args, **kwargs):
        self.turn_off_timer = None
        self.delay = 2
        self.nb_transitions = 0
        self.controler = controler
        super(DotsMachine, self).__init__(*args, **kwargs)

    def on_enter_bye(self, event, state):
        self.turn_off_timer = threading.Timer(self.delay, self.turn_off)
        self.turn_off_timer.start()

    def on_enter_state(self, event, state):
        if self.turn_off_timer is not None:
            self.turn_off_timer.cancel()
            self.turn_off_timer = None
        self.nb_transitions += 1
        print(f"On '{event}', on the '{state.id}' state.")
        #at initialization of the machine, the controler doesn't have the machine yet, 
        #but the machine enter the initial state and trigger the enter state event
        if hasattr(self.controler, 'machine'): 
            self.controler.post_process()


if __name__ == "__main__":
    m = DotsMachine(None)
    m._graph().write_png("dots_machine.png")
