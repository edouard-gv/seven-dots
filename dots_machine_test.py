import time
from statemachine import State
from dots_machine import DotsMachine

class FakeControler():
    def post_process(self):
        pass

fake_controler = FakeControler()

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
    m = DotsMachine(fake_controler, start_value="hello")
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    time.sleep(2.1)
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 3


def test_dont_turn_off_if_interupted():
    m = DotsMachine(fake_controler, start_value="hello")
    assert m.nb_transitions == 1
    m.closed_fist()
    assert m.nb_transitions == 2
    assert m.current_state.name == "Bye"
    m.open_palm()
    assert m.current_state.name == "Hello"
    time.sleep(1)
    m.closed_fist()
    time.sleep(1.1)
    assert m.current_state.name == "Bye"
    time.sleep(1)
    assert m.current_state.name == "Blank screen"
    assert m.nb_transitions == 5
