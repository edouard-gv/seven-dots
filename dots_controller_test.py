from dots_controller import SevenDotsController
from outputs.screen_output import ScreenPort


def test_screen_blank_on_startup():
    port = ScreenPort()
    main_controller = SevenDotsController()
    main_controller.append_display_from_output(port)
    main_controller.start()
    assert port.output == (" "*(7*4-1)+"\n")*(4*4-1)


if __name__ == "__main__":
    test_screen_blank_on_startup()

