from dotenv import load_dotenv

load_dotenv()

import os

from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent # .../src
INSTRUCTION_DIR = SRC_DIR / "agents" / "instructions" # .../src/agents/instructions
DOC_DIR = SRC_DIR / "output" # .../src/output

# buat pastiin environment variable yang dibutuhin ada
def _required_env(name: str) -> str:
    """Ambil env wajib, apabila gagal, tampilkan pesan error"""

    value = os.getenv(name)

    if value is None:
        raise RuntimeError(f"Environment variable {name} belum di-set")
    return value

GEMINI_API_KEY = _required_env("GEMINI_API_KEY")
GEMINI_MODEL = _required_env("GEMINI_MODEL")

SUPABASE_URL = _required_env("SUPABASE_URL")
SUPABASE_KEY = _required_env("SUPABASE_KEY")

