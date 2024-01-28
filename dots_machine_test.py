import time
from statemachine import State
from dots_machine import DotsMachine


class FakeControler:
    def post_process(self):
        pass


fake_controler = FakeControler()

# publish subscribe pattern for faking the timer
# https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern
# https://pypi.org/project/pubsub/


class Timers:
    def __init__(self):
        self.timers = []

    def tick(self):  # the publisj
        for timer in self.timers:
            timer.tick()

    def subscribe(self, timer):
        self.timers.append(timer)

    def unsubscribe(self, timer):
        self.timers.remove(timer)


def get_mocked_timer_factory(timers):
    class MockedTimer:
        def __init__(self, nb_ticks, callback):
            self.started = False
            self.cancelled = False
            self.nb_ticks = nb_ticks
            self.callback = callback
            self.timers = timers

        def start(self):
            self.started = True
            timers.subscribe(self)

        def cancel(self):
            self.cancelled = True
            if self in self.timers.timers:
                timers.unsubscribe(self)

        def tick(self):
            self.nb_ticks -= 1
            if self.nb_ticks == 0:
                timers.unsubscribe(self)
                self.callback()

    def get_mocked_timer(nb_ticks, callback):
        return MockedTimer(nb_ticks=nb_ticks, callback=callback)

    return get_mocked_timer


def test_first_transition():
    m = DotsMachine(fake_controler)
    m.open_palm()
    assert m.current_state.name == "Hello"


def test_same_state_on_hello():
    m = DotsMachine(fake_controler)

    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2
    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2


def test_before_turn_off():
    timers = Timers()
    m = DotsMachine(
        fake_controler, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    timers.tick()
    timers.tick()  # 2 seconds
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 3


def test_dont_turn_off_if_interupted():
    timers = Timers()
    m = DotsMachine(
        fake_controler, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    assert m.current_state.name == "Bye"
    m.open_palm()
    assert m.current_state.name == "Hello"
    timers.tick()
    m.closed_fist()
    timers.tick()
    assert m.current_state.name == "Bye"
    timers.tick()
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 5


def test_launch_2mins_countdown():
    timers = Timers()
    m = DotsMachine(
        fake_controler, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 120
    for _ in range(118):
        timers.tick()
    assert m.countdown_value == 2
    timers.tick()
    assert m.countdown_value == 1
    timers.tick()
    assert m.countdown_value == 0
    timers.tick()
    assert m.current_state.name == "Bye"


def test_countdown_should_be_put_in_background_until_the_end():
    timers = Timers()
    m = DotsMachine(
        fake_controler, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    assert m.current_state.name == "Countdown"
    timers.tick()
    m.open_palm()
    assert m.current_state.name == "Hello"
    for _ in range(120):
        timers.tick()


def test_countdown_cannot_be_launched_twice():
    timers = Timers()
    m = DotsMachine(
        fake_controler, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    timers.tick()
    m.open_palm()
    timers.tick()
    m.victory()  # should reset the countdown
    for _ in range(118):
        timers.tick()
    assert m.countdown_value == 2


if __name__ == "__main__":
    pass
