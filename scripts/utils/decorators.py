import psutil
import timeit
from functools import wraps

def calculate_ram_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        initial_ram_usage = psutil.Process().memory_info().rss / (1024 * 1024)
        result = func(*args, **kwargs)
        ram_usage = psutil.Process().memory_info().rss / (1024 * 1024) - initial_ram_usage
        print(f"RAM Usage: {ram_usage} MB")
        with open('ram_usage_data.txt','a') as file: file.write(f"{ram_usage}\n")
        return result
    return wrapper

def calculate_elapsed_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed_time = timeit.default_timer() - start
        print(f"Elapsed time: {elapsed_time:.4f} seconds")
        with open('elapsed_time_data.txt','a') as file: file.write(f"{elapsed_time}\n")
        return result
    return wrapper