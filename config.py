import os
from dotenv import load_dotenv

# Load environment variables
def load_config():
    print("\n[INFO] Loading environment variables...")

    # Set base directory to the current script's directory (First-Aid-Backend)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Load environment variables from .env file inside First-Aid-Backend
    env_path = os.path.join(base_dir, ".env")
    # Try loading local .env file only if it exists (for local dev)
    if os.path.exists(env_path):
        print(f"[INFO] Loading local .env file from {env_path}")
        load_dotenv(env_path)
    else:
        print("[INFO] .env file not found. Assuming environment variables are set by host (e.g., Render).")

    # Check if .env file exists
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"[ERROR] .env file not found at {env_path}. Ensure it exists!")

    load_dotenv(env_path)
    
    # Get API keys and other environment variables
    groq_api_key = os.getenv("GROQ_API_KEY")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")

    # Validate required variables
    if not groq_api_key:
        raise ValueError("[ERROR] API Key not found! Ensure the .env file contains GROQ_API_KEY.")
    if not aws_access_key_id or not aws_secret_access_key or not s3_bucket_name:
        raise ValueError("[ERROR] Missing AWS credentials or S3 bucket name in .env file!")

    # Define correct FAISS database path inside First-Aid-Backend
    db_path = os.path.join(base_dir, "data", "faiss_db")
    
    # Debugging paths
    print(f"[DEBUG] Base Directory: {base_dir}")
    print(f"[DEBUG] FAISS DB Path: {db_path}")
    
    # Ensure the 'data' directory exists
    data_path = os.path.join(base_dir, "data")
    
    if not os.path.exists(data_path):
        print(f"[INFO] Creating 'data' directory at: {data_path}")
        os.makedirs(data_path, exist_ok=True)
    else:
        print("[INFO] 'data' directory already exists.")

    if not os.path.exists(db_path):
        print(f"[INFO] Creating FAISS DB directory at: {db_path}")
        os.makedirs(db_path, exist_ok=True)
    else:
        print("[INFO] FAISS DB directory already exists.")

    print("[SUCCESS] Configuration loaded successfully!\n")
    
    # Return configuration
    return {
        "s3_bucket_name": s3_bucket_name,
        "groq_api_key": groq_api_key,
        "db_path": db_path,
        "model_name": "llama-3.3-70b-versatile",
        "temperature": 0,
        "host": "0.0.0.0",
        "port": int(os.environ.get("PORT", 5000)),
        "debug": False,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key
    }
