from dots_controller import SevenDotsController
from dots_machine_test import cancel_timers, MockedDotsMachine
from outputs.display import Display
from system_control import FakeSystemControl
from outputs.screen_output import ScreenPort


def test_screen_blank_on_startup():
    port = ScreenPort()
    c = SevenDotsController()
    c.append_display_from_output(port)
    c.start()
    assert port.output == (" "*(7*4-1)+"\n")*(4*4-1)
    cancel_timers(c.machine)


def assert_system_running(system_control):
    assert not system_control.is_shutdown() and not system_control.is_update()


def test_journey_to_shutdown_with_double_iloveyou():
    c = SevenDotsController()
    system_control = FakeSystemControl()
    c.set_system_control(system_control)
    c.start()
    assert c.machine.current_state == c.machine.blank_screen
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("pointing_up")
    assert_system_running(system_control)
    c.process_command("thumb_up")
    assert system_control.is_shutdown()
    assert c.machine.slow_pace
    cancel_timers(c.machine)


def test_journey_to_update_through_cancels():
    c = SevenDotsController()
    system_control = FakeSystemControl()
    c.set_system_control(system_control)
    c.start()
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("pointing_up")
    assert_system_running(system_control)
    c.process_command("open_palm")
    assert_system_running(system_control)
    c.process_command("victory")
    assert_system_running(system_control)
    c.process_command("open_palm")
    assert_system_running(system_control)
    c.process_command("open_palm")
    assert_system_running(system_control)
    assert c.machine.current_state == c.machine.menu_system
    c.process_command("none")
    c.process_command("open_palm")
    assert c.machine.current_state == c.machine.blank_screen
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("pointing_up")
    assert_system_running(system_control)
    c.process_command("open_palm")
    assert_system_running(system_control)
    c.process_command("victory")
    assert_system_running(system_control)
    c.process_command("thumb_up")
    assert system_control.is_update()
    assert c.machine.slow_pace
    cancel_timers(c.machine)


# cf issue #16
def test_no_blank_screen_when_starting_countdown_after_hello():
    c = SevenDotsController()
    m = MockedDotsMachine(c, start_value="hello")
    c.machine = m
    port = ScreenPort()
    c.outputs.append(Display(port))
    c.process_command("pointing_up")
    assert c.machine.current_state.value == "countdown"
    assert port.output != (" "*(7*4-1)+"\n")*(4*4-1)
    m.cancel_timers()


if __name__ == "__main__":
    test_screen_blank_on_startup()

