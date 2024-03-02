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


class MockedDotsMachine(DotsMachine):
    class __TimerBus:
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

    class __MockedTimer:
        def __init__(self, timer_bus, nb_ticks_initial, callback):
            self.nb_ticks = nb_ticks_initial
            self.callback = callback
            self.timer_bus = timer_bus
            timer_bus.subscribe(self)

        def cancel(self):
            if self in self.timer_bus.timers:
                self.timer_bus.unsubscribe(self)

        def is_alive(self):
            return self in self.timer_bus.timers

        def tick(self):
            self.nb_ticks -= 1
            if self.nb_ticks == 0:
                self.timer_bus.unsubscribe(self)
                self.callback()

    def __init__(self, controller, *args, **kwargs):
        self.__timer_bus = MockedDotsMachine.__TimerBus()
        super(MockedDotsMachine, self).__init__(controller, *args, **kwargs)

    def start_timer(self, nb_ticks, callback):
        return MockedDotsMachine.__MockedTimer(self.__timer_bus, nb_ticks_initial=nb_ticks, callback=callback)

    def tick(self, nb_ticks=1):
        self.__timer_bus.tick(nb_ticks)

    def cancel_timers(self):
        cancel_timers(self)


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
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state.name == "Hello"
    m.cancel_timers()


def test_same_state_on_hello():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2
    m.open_palm()
    assert m.current_state.name == "Hello"
    assert m.nb_transitions == 2
    m.cancel_timers()


def test_before_turn_off():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    m.tick()
    m.tick()
    m.tick()  # 2 seconds
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 3
    m.cancel_timers()


def test_dont_turn_off_if_interrupted():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    assert m.current_state.name == "Bye"
    m.open_palm()
    assert m.current_state.name == "Hello"
    m.tick()
    m.closed_fist()
    m.tick()
    assert m.current_state.name == "Bye"
    m.tick()
    m.tick()
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 6
    m.cancel_timers()


def test_launch_2mins_countdown():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 120
    m.tick(nb_ticks=118)
    assert m.countdown_value == 2
    m.tick()
    assert m.countdown_value == 1
    m.tick()
    assert m.countdown_value == 0
    m.tick()
    assert m.current_state.name == "Bye"
    m.cancel_timers()


def test_launch_1mins_countdown():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    assert m.current_state.name == "Countdown"
    assert m.countdown_value == 60
    m.tick(nb_ticks=59)
    assert m.countdown_value == 1
    m.tick()
    m.tick()
    assert m.current_state.name == "Bye"
    m.cancel_timers()


def test_countdown_should_be_put_in_background_until_the_end():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    assert m.current_state.name == "Countdown"
    m.tick()
    m.open_palm()
    assert m.current_state.name == "Countdown confirm stop"
    m.tick(nb_ticks=120)
    m.cancel_timers()


def test_when_countdown_stops_during_confirmation():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    for _ in range(119):
        m.tick()
    assert m.countdown_value == 1
    m.open_palm()
    assert m.current_state.name == "Countdown confirm stop"
    m.tick()
    m.tick()
    assert m.current_state.name == "Bye"
    m.cancel_timers()


def test_countdown_should_be_interrupted_by_bye_with_confirmation():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.open_palm()
    m.thumb_up()
    assert m.current_state.name == "Bye"
    m.turn_off_timer.cancel()
    m.cancel_timers()

def test_countdown_should_not_be_interrupted_by_bye_without_confirmation():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.tick()
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
    m.cancel_timers()


def test_increment_countdown_by_1min():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.closed_fist()
    m.pointing_up()
    assert m.countdown_value == 120
    m.cancel_timers()


def test_dont_increment_countdown_by_if_no_open_palm():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    with pytest.raises(TransitionNotAllowed):
        m.pointing_up()
    assert m.countdown_value == 60
    m.cancel_timers()


def test_increment_after_canceling_stop_countdown():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.open_palm()
    m.none()
    m.open_palm()
    m.pointing_up()
    assert m.countdown_value == 120
    m.cancel_timers()


def test_increment_countdown_by_2min():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.closed_fist()
    m.victory()
    assert m.countdown_value == 240
    m.cancel_timers()


def test_increment_countdown_by_1min_with_no_transitions_v2pu():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.pointing_up()
    assert m.countdown_value == 180
    m.cancel_timers()


def test_increment_countdown_by_1min_with_no_transitions_v2pu2v():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    m.pointing_up()
    m.victory()
    assert m.countdown_value == 300
    m.cancel_timers()


def test_increment_countdown_by_1min_with_no_transitions_pu2v():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    m.victory()
    assert m.countdown_value == 180
    m.cancel_timers()


def test_print_timer_for_one_second_after_countdown_is_set():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    assert m.show_countdown()
    m.tick()
    m.tick()
    assert not m.show_countdown()
    m.cancel_timers()


def test_no_increment_countdown_when_same_action_pu():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.pointing_up()
    with pytest.raises(TransitionNotAllowed):
        m.pointing_up()
    assert m.countdown_value == 60
    m.cancel_timers()


def test_no_increment_countdown_when_same_action_v():
    m = MockedDotsMachine(fake_controller, start_value="hello")
    m.victory()
    with pytest.raises(TransitionNotAllowed):
        m.victory()
    assert m.countdown_value == 120
    m.cancel_timers()


def test_slow_pace():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    assert m.slow_pace
    m.open_palm()
    assert not m.slow_pace
    m.cancel_timers()


def test_is_system_state():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    assert not m.is_system_state()
    m.cancel_timers()
    m = MockedDotsMachine(fake_controller, start_value="system_shutdown")
    assert m.is_system_state()
    m.cancel_timers()
    m = MockedDotsMachine(fake_controller, start_value="system_update")
    assert m.is_system_state()
    m.cancel_timers()


def test_full_meteo_cycle():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.tick()
    assert m.current_state == m.meteo_1
    m.tick()
    m.tick()
    assert m.current_state == m.meteo_2
    m.tick()
    assert m.current_state == m.meteo_2
    m.cancel_timers()


def test_meteo_interrupted_in_hello():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.pointing_up()
    assert m.current_state == m.countdown
    m.tick()
    assert m.current_state == m.countdown
    m.tick()
    assert m.current_state == m.countdown
    m.cancel_timers()


def test_meteo_interrupted_in_first_view():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.tick()
    m.pointing_up()
    assert m.current_state == m.countdown
    m.tick()
    assert m.current_state == m.countdown
    m.cancel_timers()


def test_meteo_interrupted_in_second_view():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.tick()
    m.tick()
    m.pointing_up()
    assert m.current_state == m.countdown
    m.cancel_timers()


def test_standby():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.tick(3)
    assert m.current_state == m.meteo_2
    m.tick(5*60-1)
    assert m.current_state == m.meteo_2
    m.tick()
    assert m.current_state == m.blank_screen
    m.cancel_timers()


def test_standby_is_postponed_on_action():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.tick(5)
    m.closed_fist()
    m.open_palm()
    m.tick(3)
    assert m.current_state == m.meteo_2
    m.tick(5*60-1)
    assert m.current_state == m.meteo_2
    m.tick()
    assert m.current_state == m.blank_screen
    m.cancel_timers()


def test_standby_does_not_affect_countdown():
    m = MockedDotsMachine(fake_controller, start_value="blank_screen")
    m.open_palm()
    assert m.current_state == m.hello
    m.tick(5)
    m.closed_fist()
    m.open_palm()
    m.victory()
    m.closed_fist()
    m.victory()
    m.closed_fist()
    m.victory()  # 3*120 = 6 minutes > 5 minutes
    m.tick(5*60+30)
    assert m.current_state == m.countdown
    m.cancel_timers()


if __name__ == "__main__":
    pass
