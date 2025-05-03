from functools import wraps
import time

def time_function(func):
    """
    A decorator to measure the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Capture the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Capture the end time
        execution_time = end_time - start_time  # Calculate the execution time
        print(f"Function {func.__name__} executed in {execution_time:.4f} seconds.")
        return result

    return wrapper