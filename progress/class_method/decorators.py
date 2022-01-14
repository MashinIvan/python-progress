import functools
import typing
import time

from progress.classes.progress import Progress, ProgressWithTime


def progress(
        *,
        total: str = None,
        estimate_time: bool = False,
        same_line: bool = True,
        length: int = 30,
        fill: str = '#',
        empty: str = ' ',
) -> typing.Callable:
    def decorator(
            func: typing.Union[
                typing.Generator[typing.Any, typing.Any, typing.Any],
                typing.Callable
            ]
    ) -> typing.Callable:

        @functools.wraps(func)
        def wrapper_default(self, *args, **kwargs) -> typing.Any:
            progress_obj = Progress(getattr(self, total), same_line, length, fill, empty)

            generator = func(self, *args, **kwargs)
            progress_obj.print(same_line=False)
            try:
                while True:
                    increment = next(generator)
                    if not increment:
                        increment = 1
                    progress_obj.increment(increment)

                    progress_obj.print()
            except StopIteration as result:
                progress_obj.print()
                return result.value

        @functools.wraps(func)
        def wrapper_time_estimate(self, *args, **kwargs) -> typing.Any:
            progress_obj = ProgressWithTime(getattr(self, total), same_line, length, fill, empty)

            generator = func(self, *args, **kwargs)
            progress_obj.print(same_line=False)
            try:
                times = []
                while True:
                    t = time.time()
                    increment = next(generator)
                    if not increment:
                        increment = 1
                    progress_obj.increment(increment)

                    iteration_time = time.time() - t
                    times.append(iteration_time)
                    progress_obj.calculate_remaining_time(times)

                    progress_obj.print()

            except StopIteration as result:
                progress_obj.print()
                return result.value

        if estimate_time:
            return wrapper_time_estimate
        return wrapper_default

    return decorator
