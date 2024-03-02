import pytest
from statemachine.exceptions import TransitionNotAllowed

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
            self.started = True
            self.cancelled = False
            self.nb_ticks = nb_ticks
            self.callback = callback
            self.timers = timers
            timers.subscribe(self)

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

    return lambda nb_ticks, callback: MockedTimer(nb_ticks=nb_ticks, callback=callback)


def cancel_timers(m):
    if m.turn_off_timer is not None:
        m.turn_off_timer.cancel()
    if m.hello_timer is not None:
        m.hello_timer.cancel()
    if m.countdown_timer is not None:
        m.countdown_timer.cancel()
    if m.standby_timer is not None:
        m.standby_timer.cancel()


def test_first_transition():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state.name == "Hello"
    cancel_timers(m)


def test_same_state_on_hello():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2
    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2
    cancel_timers(m)


def test_before_turn_off():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    timers.tick()
    timers.tick()
    timers.tick()  # 2 seconds
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 3
    cancel_timers(m)


def test_dont_turn_off_if_interrupted():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
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
    timers.tick()
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 6
    cancel_timers(m)


def test_launch_2mins_countdown():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
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
    cancel_timers(m)


def test_launch_1mins_countdown():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
    m.pointing_up()
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 60
    timers.tick(nb_ticks=59)
    assert m.countdown_value == 1
    timers.tick()
    timers.tick()
    assert m.current_state.name == "Bye"
    cancel_timers(m)


def test_countdown_should_be_put_in_background_until_the_end():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
    m.victory()
    assert m.current_state.name == "Countdown"
    timers.tick()
    m.open_palm()
    assert m.current_state.name == "Countdown confirm stop"
    timers.tick(nb_ticks=120)
    cancel_timers(m)


def test_when_countdown_stops_during_confirmation():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
    m.victory()
    for _ in range(119):
        timers.tick()
    assert m.countdown_value == 1
    m.open_palm()
    assert m.current_state.name == "Countdown confirm stop"
    timers.tick()
    timers.tick()
    assert m.current_state.name == "Bye"
    cancel_timers(m)


def test_countdown_should_be_interrupted_by_bye_with_confirmation():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.open_palm()
    m.thumb_up()
    assert m.current_state.name == "Bye"
    m.turn_off_timer.cancel()
    cancel_timers(m)

def test_countdown_should_not_be_interrupted_by_bye_without_confirmation():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
    m.victory()
    timers.tick()
    m.open_palm()
    assert m.current_state.name == "Countdown confirm stop"
    m.none()
    m.open_palm()
    m.open_palm()
    assert m.countdown_running()
    assert m.current_state.name == "Countdown accept increment"
    assert m.countdown_value == 119
    m.none()
    m.open_palm()
    assert m.current_state.name == "Countdown confirm stop"
    cancel_timers(m)


def test_increment_countdown_by_1min():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.closed_fist()
    m.pointing_up()
    assert m.countdown_value == 120
    cancel_timers(m)


def test_dont_increment_countdown_by_if_no_open_palm():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    with pytest.raises(TransitionNotAllowed):
        m.pointing_up()
    assert m.countdown_value == 60
    cancel_timers(m)


def test_increment_after_canceling_stop_countdown():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.open_palm()
    m.none()
    m.open_palm()
    m.pointing_up()
    assert m.countdown_value == 120
    cancel_timers(m)


def test_increment_countdown_by_2min():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.closed_fist()
    m.victory()
    assert m.countdown_value == 240
    cancel_timers(m)


def test_increment_countdown_by_1min_with_no_transitions_v2pu():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.pointing_up()
    assert m.countdown_value == 180
    cancel_timers(m)


def test_increment_countdown_by_1min_with_no_transitions_v2pu2v():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.pointing_up()
    m.victory()
    assert m.countdown_value == 300
    cancel_timers(m)


def test_increment_countdown_by_1min_with_no_transitions_pu2v():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.victory()
    assert m.countdown_value == 180
    cancel_timers(m)


def test_print_timer_for_one_second_after_countdown_is_set():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="hello")
    m.start_timer = get_mocked_timer_factory(timers)
    m.victory()
    assert m.show_countdown()
    timers.tick()
    timers.tick()
    assert not m.show_countdown()
    cancel_timers(m)


def test_no_increment_countdown_when_same_action_pu():
    m = DotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    with pytest.raises(TransitionNotAllowed):
        m.pointing_up()
    assert m.countdown_value == 60
    cancel_timers(m)


def test_no_increment_countdown_when_same_action_v():
    m = DotsMachine(fake_controller, start_value="hello")
    m.victory()
    with pytest.raises(TransitionNotAllowed):
        m.victory()
    assert m.countdown_value == 120
    cancel_timers(m)


def test_slow_pace():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    assert m.slow_pace
    m.open_palm()
    assert not m.slow_pace
    cancel_timers(m)


def test_is_system_state():
    m = DotsMachine(fake_controller, start_value="blank_screen")
    assert not m.is_system_state()
    cancel_timers(m)
    m = DotsMachine(fake_controller, start_value="system_shutdown")
    assert m.is_system_state()
    cancel_timers(m)
    m = DotsMachine(fake_controller, start_value="system_update")
    assert m.is_system_state()
    cancel_timers(m)


def test_full_meteo_cycle():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    timers.tick()
    assert m.current_state == m.meteo_1
    timers.tick()
    timers.tick()
    assert m.current_state == m.meteo_2
    timers.tick()
    assert m.current_state == m.meteo_2
    cancel_timers(m)


def test_meteo_interrupted_in_hello():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    m.pointing_up()
    assert m.current_state == m.countdown
    timers.tick()
    assert m.current_state == m.countdown
    timers.tick()
    assert m.current_state == m.countdown
    cancel_timers(m)


def test_meteo_interrupted_in_first_view():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    timers.tick()
    m.pointing_up()
    assert m.current_state == m.countdown
    timers.tick()
    assert m.current_state == m.countdown
    cancel_timers(m)


def test_meteo_interrupted_in_second_view():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    timers.tick()
    timers.tick()
    m.pointing_up()
    assert m.current_state == m.countdown
    cancel_timers(m)


def test_standby():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    timers.tick(3)
    assert m.current_state == m.meteo_2
    timers.tick(5*60-1)
    assert m.current_state == m.meteo_2
    timers.tick()
    assert m.current_state == m.blank_screen
    cancel_timers(m)


def test_standby_is_postponed_on_action():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    timers.tick(5)
    m.closed_fist()
    m.open_palm()
    timers.tick(3)
    assert m.current_state == m.meteo_2
    timers.tick(5*60-1)
    assert m.current_state == m.meteo_2
    timers.tick()
    assert m.current_state == m.blank_screen
    cancel_timers(m)


def test_standby_does_not_affect_countdown():
    timers = Timers()
    m = DotsMachine(fake_controller, start_value="blank_screen")
    m.start_timer = get_mocked_timer_factory(timers)
    m.open_palm()
    assert m.current_state == m.hello
    timers.tick(5)
    m.closed_fist()
    m.open_palm()
    m.victory()
    m.closed_fist()
    m.victory()
    m.closed_fist()
    m.victory()  # 3*120 = 6 minutes > 5 minutes
    timers.tick(5*60+30)
    assert m.current_state == m.countdown
    cancel_timers(m)


if __name__ == "__main__":
    pass
