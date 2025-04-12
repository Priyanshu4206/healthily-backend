import os
from dotenv import load_dotenv

def load_config():
    print("\n[INFO] Loading environment variables...")

    # Set base directory to the current script's directory (First-Aid-Backend)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define path to .env
    env_path = os.path.join(base_dir, ".env")

    # Load local .env file if it exists (useful for local dev)
    if os.path.exists(env_path):
        print(f"[INFO] Found .env file at {env_path}, loading...")
        load_dotenv(env_path)
    else:
        print("[INFO] No local .env file found. Assuming environment variables are provided by the deployment host (e.g., Render).")

    # Fetch required environment variables
    groq_api_key = os.getenv("GROQ_API_KEY")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")

    # Validate environment variables
    if not groq_api_key:
        raise ValueError("[ERROR] Missing GROQ_API_KEY environment variable.")
    if not aws_access_key_id or not aws_secret_access_key or not s3_bucket_name:
        raise ValueError("[ERROR] Missing AWS credentials or S3_BUCKET_NAME in environment variables.")

    # Define FAISS database path
    data_path = os.path.join(base_dir, "data")
    db_path = os.path.join(data_path, "faiss_db")

    # Ensure directories exist
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

    # Debug paths
    print(f"[DEBUG] Base Directory: {base_dir}")
    print(f"[DEBUG] FAISS DB Path: {db_path}")
    print("[SUCCESS] Configuration loaded successfully!\n")

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
