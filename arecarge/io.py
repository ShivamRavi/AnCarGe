
from collections import deque

class IO:
    def prompt(self, msg: str) -> str:
        """ummm u told me to make an io """
        raise NotImplementedError

    def display(self, msg: str) -> None:
        """msg. show. ez."""
        raise NotImplementedError


class ConsoleIO(IO):
    def prompt(self, msg: str | None) -> str:
        return input(msg)

    def display(self, msg: str, **kwargs) -> None:
        print(msg, **kwargs)


def get_ioc():
    return ConsoleIO()


class TestIO(IO):
    def __init__(self, inputs):
        self.inputs = deque(inputs)
        self.outputs = []

    def prompt(self, msg: str):
        if self.inputs:
            return self.inputs.popleft()
        else:
            raise Exception("No more inputs available")
    def display(self, msg: str):
        self.outputs.append(msg)