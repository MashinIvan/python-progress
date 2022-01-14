import dataclasses
import logging
import typing
import time


logger = logging.getLogger("")


@dataclasses.dataclass
class Spinner:
    symbols: typing.Union[typing.List[str], typing.Tuple]
    same_line: bool

    _format: str = "{prefix}Running {spinner}"
    _current: int = 0
    _finished: bool = False

    def start(self) -> None:
        self.print(same_line=False)
        while not self._finished:
            time.sleep(0.5)
            self.increment()
            self.print()

    def finish(self) -> None:
        self._finished = True

    def print(self, same_line: bool = None) -> None:
        if same_line is None:
            same_line = self.same_line
        logger.info(
            self._format.format(
                prefix="\r" if same_line else "\n",
                spinner=self.symbols[self._current],
            ),
        )

    def increment(self) -> None:
        self._current = (self._current + 1) % len(self.symbols)


@dataclasses.dataclass
class SpinnerWithTimer(Spinner):
    _format: str = "{prefix}Running {spinner}  time: {time}"
    _start_time: float = ''

    def start(self) -> None:
        self._start_time = time.time()

        self.print(same_line=False)
        while not self._finished:
            time.sleep(0.5)
            self.print()
            self.increment()

    def print(self, same_line: bool = None) -> None:
        if same_line is None:
            same_line = self.same_line
        logger.info(
            self._format.format(
                prefix="\r" if same_line else "\n",
                spinner=self.symbols[self._current],
                time=self._time_passed,
            ),
        )

    @property
    def _time_passed(self) -> str:
        total_seconds = time.time() - self._start_time
        seconds = total_seconds % 60
        minutes = total_seconds // 60
        return "{:02d}:{:02d}".format(int(minutes), int(seconds))
