import dataclasses
import typing


@dataclasses.dataclass
class Progress:
    total: int

    end: str
    length: int
    fill: str
    empty: str

    _format = "[{fill}{empty}] {percent:.2f}%"
    _current: int = 0

    def print(self, end: str = None) -> None:
        if not end:
            end = self.end
        print(
            self._format.format(
                fill=self._fill_number*self.fill,
                empty=self._empty_number*self.empty,
                percent=self._percent * 100,
            ),
            end=end
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
    _format = "[{fill}{empty}] {percent:.2f}% | approximated time: {time}"

    def print(self, end: str = None) -> None:
        if not end:
            end = self.end
        print(
            self._format.format(
                fill=self._fill_number*self.fill,
                empty=self._empty_number*self.empty,
                percent=self._percent * 100,
                time=self._remaining_time,
            ),
            end=end,
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
