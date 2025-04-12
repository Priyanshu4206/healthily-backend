import os
from dotenv import load_dotenv

# Load environment variables
def load_config():
    print("\n[INFO] Loading environment variables...")

    # Set base directory to the current script's directory (First-Aid-Backend)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Load environment variables from .env file inside First-Aid-Backend
    env_path = os.path.join(base_dir, ".env")
    print(f"[DEBUG] Looking for .env file at: {env_path}")
    load_dotenv(env_path)
    
    # Get API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("[ERROR] API Key not found! Ensure the .env file exists and contains GROQ_API_KEY.")
    
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
        "groq_api_key": groq_api_key,
        "db_path": db_path,
        "model_name": "llama-3.3-70b-versatile",
        "temperature": 0,
        "host": "0.0.0.0",
        "port": int(os.environ.get("PORT", 5000)),
        "debug": False
    }
