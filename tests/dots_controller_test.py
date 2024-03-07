from dots_controller import SevenDotsController
from dots_machine_test import cancel_timers, MockedDotsMachine
from inputs.motion_sensor_input import FakeMotionSensor
from inputs.video_input import VideoInput
from outputs.display import Display
from outputs.screen_output import ScreenPort
from system_control import FakeSystemControl


class MockedMotionSensorInput(FakeMotionSensor):

    def start(self, controller):
        pass

    def wake_up(self, controller):
        super(MockedMotionSensorInput, self)._wake_up(controller)


class MockedVideoInput(VideoInput):

    def __init__(self):
        self.force_stop = False

    def start(self, controller):
        self.force_stop = False

    def stop(self):
        self.force_stop = True


def test_screen_blank_on_startup():
    port = ScreenPort()
    c = SevenDotsController()
    c.input = MockedVideoInput()
    c.append_display_from_output(port)
    c.start()
    assert port.output == (" " * (7 * 4 - 1) + "\n") * (4 * 4 - 1)
    cancel_timers(c.machine)


def assert_system_running(system_control):
    assert not system_control.is_shutdown() and not system_control.is_update()


def test_journey_to_shutdown_with_double_iloveyou():
    c = SevenDotsController()
    c.input = MockedVideoInput()
    system_control = FakeSystemControl()
    c.system_control = system_control
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
    cancel_timers(c.machine)


def test_journey_to_update_through_cancels():
    c = SevenDotsController()
    c.input = MockedVideoInput()
    system_control = FakeSystemControl()
    c.system_control = system_control
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
    cancel_timers(c.machine)


# cf issue #16
def test_no_blank_screen_when_starting_countdown_after_hello():
    c = SevenDotsController()
    c.input = MockedVideoInput()
    m = MockedDotsMachine(c, start_value="hello")
    c.machine = m
    port = ScreenPort()
    c.outputs.append(Display(port))
    c.process_command("pointing_up")
    assert c.machine.current_state.value == "countdown"
    assert port.output != (" " * (7 * 4 - 1) + "\n") * (4 * 4 - 1)
    m.cancel_timers()


def test_standby_and_wakeup():
    controller = SevenDotsController()
    machine = MockedDotsMachine(controller, start_value="hello")
    controller.machine = machine
    video_input = MockedVideoInput()
    controller.input = video_input
    sensor = MockedMotionSensorInput()
    controller.sensor = sensor
    machine.tick(5*60+3)
    assert machine.current_state == machine.standby_screen
    assert video_input.force_stop
    sensor.wake_up(controller)
    assert machine.current_state == machine.blank_screen
    assert not video_input.force_stop
    machine.cancel_timers()


def test_dont_standby_if_motion():
    controller = SevenDotsController()
    machine = MockedDotsMachine(controller, start_value="hello")
    controller.machine = machine
    video_input = MockedVideoInput()
    controller.input = video_input
    sensor = MockedMotionSensorInput()
    controller.sensor = sensor
    sensor.motion_detected = lambda: True
    machine.tick(5*60+3)
    assert machine.current_state == machine.meteo_2
    sensor.motion_detected = lambda: False
    machine.tick(5*60+3)
    assert machine.current_state == machine.standby_screen
    machine.cancel_timers()

