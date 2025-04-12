import os
import time
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

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

def download_from_s3(bucket, s3_path, local_path, aws_access_key_id, aws_secret_access_key):
    """Download a file from S3 to a local directory"""
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    try:
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            print(f"Created local directory: {os.path.dirname(local_path)}")

        print(f"[INFO] Downloading from S3: {bucket}/{s3_path} to {local_path}")
        s3.download_file(bucket, s3_path, local_path)
        print(f"[SUCCESS] File downloaded successfully from S3.")
    
    except NoCredentialsError:
        print("[ERROR] AWS credentials not found or invalid.")
    except PartialCredentialsError:
        print("[ERROR] Incomplete AWS credentials.")
    except FileNotFoundError:
        print(f"[ERROR] The specified file {s3_path} does not exist in S3.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")