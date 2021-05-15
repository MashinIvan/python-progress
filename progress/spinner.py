import dataclasses
import typing
import time


@dataclasses.dataclass
class Spinner:
    symbols: typing.Union[typing.List[str], typing.Tuple]
    end: str

    _format: str = "Running {spinner}"
    _current: int = 0
    _finished: bool = False

    def start(self) -> None:
        while not self._finished:
            self.print()
            self.increment()
            time.sleep(0.5)

    def finish(self) -> None:
        self._finished = True

    def print(self, end: str = None) -> None:
        if not end:
            end = self.end
        print(
            self._format.format(
                spinner=self.symbols[self._current],
            ),
            end=end,
        )

    def increment(self) -> None:
        self._current = (self._current + 1) % len(self.symbols)


@dataclasses.dataclass
class SpinnerWithTimer(Spinner):
    _format: str = "Running {spinner}  time: {time}"
    _start_time: float = ''

    def start(self) -> None:
        self._start_time = time.time()

        while not self._finished:
            self.print()
            self.increment()
            time.sleep(0.5)

    def print(self, end: str = None) -> None:
        if not end:
            end = self.end
        print(
            self._format.format(
                spinner=self.symbols[self._current],
                time=self._time_passed,
            ),
            end=end,
        )

    @property
    def _time_passed(self) -> str:
        total_seconds = time.time() - self._start_time
        seconds = total_seconds % 60
        minutes = total_seconds // 60
        return "{:02d}:{:02d}".format(int(minutes), int(seconds))
