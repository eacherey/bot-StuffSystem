import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} must be set.")
    return value

def get_required_int_env(name: str) -> int:
    value = get_required_env(name)
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"Environment variable {name} must be an integer.")

TOKEN = get_required_env("TOKEN")
DB_PATH = get_required_env("DB_PATH")
HELPER_ID = get_required_int_env("HELPER_ID")
MODER_ID = get_required_int_env("MODER_ID")
LOG_CHANNEL_ID = get_required_int_env("LOG_CHANNEL_ID")
