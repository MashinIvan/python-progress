from progress.progress import Progress, ProgressWithTime
from progress.spinner import Spinner, SpinnerWithTimer

import functools
import threading
import typing
import time


def progress(
        *,
        total: int,
        estimate_time: bool = False,
        end: str = '\r',
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
        def wrapper_default(*args, **kwargs) -> typing.Any:
            generator = func(*args, **kwargs)
            progress_obj.print()
            try:
                while True:
                    increment = next(generator)
                    if not increment:
                        increment = 1
                    progress_obj.increment(increment)

                    progress_obj.print()
            except StopIteration as result:
                progress_obj.print(end='\n')
                return result.value

        @functools.wraps(func)
        def wrapper_time_estimate(*args, **kwargs) -> typing.Any:
            generator = func(*args, **kwargs)
            progress_obj.print()
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
                progress_obj.print(end='\n')
                return result.value

        if estimate_time:
            progress_obj = ProgressWithTime(total, end, length, fill, empty)
            return wrapper_time_estimate

        progress_obj = Progress(total, end, length, fill, empty)
        return wrapper_default

    return decorator


def spinner(
        symbols: typing.List[str] = ('\\', '|', '/', '—'),
        execution_time: bool = False,
        end: str = '\r'
) -> typing.Callable:
    def decorator(func: typing.Callable) -> typing.Callable:

        @functools.wraps(func)
        def wrapper_default(*args, **kwargs) -> typing.Any:
            spinner_thread = threading.Thread(target=progress_obj.start, daemon=True)
            spinner_thread.start()
            ret = func(*args, **kwargs)
            progress_obj.finish()
            print(end='\n')

            return ret

        if execution_time:
            progress_obj = SpinnerWithTimer(symbols, end)
        else:
            progress_obj = Spinner(symbols, end)
        return wrapper_default

    if callable(symbols):
        function = symbols
        symbols = ('\\', '|', '/', '—')
        end = '\r'
        return decorator(function)

    return decorator
