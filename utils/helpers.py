import os
import time

def log_timing(func):
    """Decorator to log the execution time of a function"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
        return result
    return wrapper

def ensure_directory_exists(directory_path):
    """Ensure that a directory exists, creating it if necessary"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory: {directory_path}")
    return directory_path