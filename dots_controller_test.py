from dots_controller import SevenDotsController
from system_control import FakeSystemControl
from outputs.screen_output import ScreenPort


def test_screen_blank_on_startup():
    port = ScreenPort()
    c = SevenDotsController()
    c.append_display_from_output(port)
    c.start()
    assert port.output == (" "*(7*4-1)+"\n")*(4*4-1)


def assert_system_running(system_control):
    assert not system_control.is_shutdown() and not system_control.is_update()


def test_journey_to_shutdown_with_double_iloveyou():
    c = SevenDotsController()
    system_control = FakeSystemControl()
    c.set_system_control(system_control)
    c.start()
    assert c.machine.current_state.value == "blank_screen"
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("pointing_up")
    assert_system_running(system_control)
    c.process_command("thumb_up")
    assert system_control.is_shutdown()
    assert c.machine.slow_pace


def test_journey_to_update_through_cancels():
    c = SevenDotsController()
    system_control = FakeSystemControl()
    c.set_system_control(system_control)
    c.start()
    c.process_command("iloveyou")
    assert_system_running(system_control)
    c.process_command("pointing_up")
    assert_system_running(system_control)
    c.process_command("thumb_down")
    assert_system_running(system_control)
    c.process_command("victory")
    assert_system_running(system_control)
    c.process_command("thumb_down")
    assert_system_running(system_control)
    c.process_command("pointing_up")
    assert_system_running(system_control)
    c.process_command("thumb_down")
    assert_system_running(system_control)
    c.process_command("victory")
    assert_system_running(system_control)
    c.process_command("thumb_up")
    assert system_control.is_update()
    assert c.machine.slow_pace


if __name__ == "__main__":
    test_screen_blank_on_startup()

