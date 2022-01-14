# Simple progress bar and spinner function wrappers

## Introduction
To wrap a function with progress bar, specify the number of iterations with **total** argument. The function must
**yield** a value to increment progress by that value or None to increment by 1. The function may return a value.

To wrap a function with spinner, there is no need to modify function in any way, just use **spinner** decorator. 

--- 

## Examples
Simplest progress bar:

```python

from progress.classes import progress
import time


@progress(total=50)
def example_progress():
    for i in range(50):
        time.sleep(0.1)
        yield
    return 1
```

Progress bar with remaining time estimation:
```python
@progress(total=50, estimate_time=True)
def example_progress():
    for i in range(50):
        time.sleep(0.1)
        yield
    return 1
```

Simplest spinner:

```python

from progress.classes import spinner


@spinner
def example_spinner():
    ...
```

Spinner with execution time:
```python
@spinner(execution_time=True)
def example_spinner_with_time():
   ...
```


Progress bar on class method with total as self attribute

```python

from progress.classes import progress as class_progress


class ExampleClassMethod:
    def __init__(self):
        self.number_of_iterations = 50

    @class_progress(total='number_of_iterations', estimate_time=True)
    def run(self):
        for i in range(self.number_of_iterations):
            time.sleep(0.1)
            yield
        return 1
```

## Customization
Customizable attributes for progress bar:
```python
fill: str = '#'
empty: str = ' '
end: str = '\r'
length: int = 30
```

Customizable attributes for spinner:
```python
symbols: tuple | list = ('\\', '|', '/', '—')
```
