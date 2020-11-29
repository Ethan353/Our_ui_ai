
import time

spend_time_table = {}


def span_time(func):
    def log_time(*args, **kwargs):
        start_time = time.time() * 1000
        result = func(*args, **kwargs)
        spend_time = (time.time() * 1000) - start_time
        print(f"Function '{func.__qualname__}' takes: {spend_time}")
        total_spend_time = spend_time_table.get(func.__qualname__, 0)
        total_spend_time += spend_time
        spend_time_table[func.__qualname__] = total_spend_time
        print(f"Total for function '{func.__qualname__}' is {total_spend_time}")
        return result

    return log_time

