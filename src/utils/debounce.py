from functools import wraps

from PySide6.QtCore import QTimer


def debounce(ms):
    """
    Decorator that will postpone a function's execution until after `ms`
    milliseconds have elapsed since the last time it was invoked.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If the wrapper is called on an instance, self will be the first argument
            if args and hasattr(args[0], "__dict__"):
                self = args[0]
            else:
                self = wrapper  # Fallback for functions not in a class

            # Use a unique attribute on the instance to store the timer
            timer_attr = f"_debounce_timer_{func.__name__}"

            # Clear previous timer if it exists
            if hasattr(self, timer_attr):
                getattr(self, timer_attr).stop()

            # Create a new timer
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: func(*args, **kwargs))

            # Store the timer on the instance
            setattr(self, timer_attr, timer)

            timer.start(ms)

        return wrapper

    return decorator
