import src.core.env as env

from pathlib import Path

from functools import lru_cache

@lru_cache
def load_instruction(name: str):
    """Baca file instruksi berdasarkan nama file, contoh: load_instruction('agent-lead')"""

    path = env.INSTRUCTION_DIR / f"{name}.md"

    # jaga" kalo file gada/typo
    if not path.exists():
        raise FileNotFoundError(
            f"File instruksi tidak ditemukan: {path}. \n"
            f"Cek nama file di {env.INSTRUCTION_DIR}"
        )

    return path.read_text(encoding="utf-8")
    



