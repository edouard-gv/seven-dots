from dots_machine import DotsMachine


class FakeController:
    def process_state(self):
        pass


fake_controller = FakeController()


# publish subscribe pattern for faking the timer
# https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern
# https://pypi.org/project/pubsub/


class Timers:
    def __init__(self):
        self.timers = []

    def tick(self, nb_ticks=1):  # the publish
        for _ in range(nb_ticks):
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
            if self.nb_ticks == 0:
                timers.unsubscribe(self)
                self.callback()

        def cancel(self):
            self.cancelled = True
            if self in self.timers.timers:
                timers.unsubscribe(self)

        def is_alive(self):
            return self.started and not self.cancelled

        def tick(self):
            self.nb_ticks -= 1
            if self.nb_ticks == 0:
                timers.unsubscribe(self)
                self.callback()

    def get_mocked_timer(nb_ticks, callback):
        return MockedTimer(nb_ticks=nb_ticks, callback=callback)

    return get_mocked_timer


def test_first_transition():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state.name == "Hello"


def test_same_state_on_hello():
    m = DotsMachine(fake_controller, start_value="blank_screen")

    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2
    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2


def test_before_turn_off():
    timers = Timers()
    m = DotsMachine(
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
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
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
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
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 120
    timers.tick(nb_ticks=118)
    assert m.countdown_value == 2
    timers.tick()
    assert m.countdown_value == 1
    timers.tick()
    assert m.countdown_value == 0
    timers.tick()
    assert m.current_state.name == "Bye"


def test_launch_1mins_countdown():
    timers = Timers()
    m = DotsMachine(
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.pointing_up()
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 60
    timers.tick(nb_ticks=59)
    assert m.countdown_value == 1
    timers.tick()
    timers.tick()
    assert m.current_state.name == "Bye"


def test_countdown_should_be_put_in_background_until_the_end():
    timers = Timers()
    m = DotsMachine(
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    assert m.current_state.name == "Countdown"
    timers.tick()
    m.open_palm()
    assert m.current_state.name == "Hello"
    timers.tick(nb_ticks=120)


def test_when_countdown_stops_during_confirmation():
    timers = Timers()
    m = DotsMachine(
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    for _ in range(119):
        timers.tick()
    assert m.countdown_value == 1
    m.closed_fist()
    assert m.current_state.name == "Countdown confirm stop"
    timers.tick()
    timers.tick()
    timers.tick()
    assert m.current_state.name == "Bye"


def test_countdown_should_be_interrupted_by_bye_with_confirmation():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.closed_fist()
    m.thumb_up()
    assert m.current_state.name == "Bye"


def test_countdown_should_not_be_interrupted_by_bye_without_confirmation():
    timers = Timers()
    m = DotsMachine(
        fake_controller, get_timer=get_mocked_timer_factory(timers), start_value="hello"
    )
    m.victory()
    timers.tick()
    m.closed_fist()
    m.thumb_down()
    assert m.countdown_running() == True
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 119
    m.countdown_timer.cancel()


def test_countdown_should_be_interrupted_by_bye_in_all_states():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.open_palm()
    m.closed_fist()
    m.thumb_up()
    assert m.countdown_running() == False
    assert m.current_state.name == "Bye"


def test_increment_countdown_by_1min():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.open_palm()
    m.pointing_up()
    assert m.countdown_value == 120


def test_increment_countdown_by_2min():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.open_palm()
    m.victory()
    assert m.countdown_value == 240


def test_increment_countdown_by_2min_with_none():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.none()
    m.victory()
    assert m.countdown_value == 240


def test_increment_countdown_by_1min_with_no_transitions_v2pu():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.pointing_up()
    assert m.countdown_value == 180


def test_increment_countdown_by_1min_with_no_transitions_pu2v():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.victory()
    assert m.countdown_value == 180


def test_no_increment_countdown_when_same_action_pu():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.pointing_up()
    assert m.countdown_value == 60


def test_no_increment_countdown_when_same_action_v():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.victory()
    assert m.countdown_value == 120


def test_same_state_for_none():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.none()
    nb_transitions = m.nb_transitions
    m.none()
    assert nb_transitions == m.nb_transitions


def test_slow_pace():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    assert m.slow_pace
    m.open_palm()
    assert not m.slow_pace


def test_is_system_state():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    assert not m.is_system_state()
    m = DotsMachine(fake_controller, start_value="system_shutdown")
    assert m.is_system_state()
    m = DotsMachine(fake_controller, start_value="system_update")
    assert m.is_system_state()


if __name__ == "__main__":
    pass
