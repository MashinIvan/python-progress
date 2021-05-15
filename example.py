from progress.decorators import progress, spinner
from classmethod.decorators import progress as class_progress
import time


@progress(total=50)
def example_progress():
    for i in range(50):
        time.sleep(0.1)
        yield
    return 1


@progress(total=50, estimate_time=True)
def example_progress_with_time():
    for i in range(50):
        time.sleep(0.1)
        yield
    return 1


@spinner
def example_spinner():
    for i in range(50):
        time.sleep(0.1)
    return 1


@spinner(execution_time=True)
def example_spinner_with_time():
    for i in range(50):
        time.sleep(0.1)
    return 1


class ExampleClassMethod:
    def __init__(self):
        self.total = 50

    @class_progress(total='total', estimate_time=True)
    def run(self):
        for i in range(self.total):
            time.sleep(0.1)
            yield
        return 1


if __name__ == '__main__':
    example_progress()
    example_progress_with_time()

    example_spinner()
    example_spinner_with_time()

    test = ExampleClassMethod()
    test.run()

