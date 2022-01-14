import dataclasses
import typing

from progress.logger import get_logger


logger = get_logger()


@dataclasses.dataclass
class Progress:
    total: int

    same_line: bool
    length: int
    fill: str
    empty: str

    _format = "{prefix}[{fill}{empty}] {percent:.2f}%"
    _current: int = 0

    def print(self, same_line: bool = None) -> None:
        if same_line is None:
            same_line = self.same_line
        logger.info(
            self._format.format(
                prefix="\r" if same_line else "\n",
                fill=self._fill_number*self.fill,
                empty=self._empty_number*self.empty,
                percent=self._percent * 100,
            ),
        )

    def increment(self, value: int) -> None:
        self._current += value

    @property
    def _percent(self) -> float:
        return self._current / self.total

    @property
    def _fill_number(self) -> int:
        return min(int(self._percent * self.length), self.length)

    @property
    def _empty_number(self) -> int:
        return self.length - self._fill_number


@dataclasses.dataclass
class ProgressWithTime(Progress):
    _remaining_time: str = '—'
    _format = "{prefix}[{fill}{empty}] {percent:.2f}% | approximated time: {time}"

    def print(self, same_line: bool = None) -> None:
        if same_line is None:
            same_line = self.same_line
        logger.info(
            self._format.format(
                prefix="\r" if same_line else "\n",
                fill=self._fill_number*self.fill,
                empty=self._empty_number*self.empty,
                percent=self._percent * 100,
                time=self._remaining_time,
            ),
        )

    def calculate_remaining_time(self, times: typing.List[float]) -> None:
        total_seconds = (self.total - self._current) * sum(times) / len(times)
        seconds = total_seconds % 60
        minutes = total_seconds // 60
        hours = minutes // 60*60

        seconds_str = "{:02d}".format(int(seconds))
        minutes_str = "{:02d}:".format(int(minutes)) if hours or minutes else "00:"
        hours_str = "{:02d}:".format(int(hours)) if hours else ""

        self._remaining_time = hours_str + minutes_str + seconds_str
