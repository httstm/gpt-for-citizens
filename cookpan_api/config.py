from pathlib import Path
import os


def get_config(key: str) -> str:
    # 1. 環境変数を優先
    value = os.getenv(key)
    if value:
        return value

    # 2. ローカル秘密ファイル
    secret_file = Path(__file__).resolve().parents[2] / "secrets" / "cookpan.txt"

    if not secret_file.exists():
        raise RuntimeError(f"{secret_file} が見つかりません")

    config = {}

    for line in secret_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        k, v = line.split("=", 1)
        config[k.strip()] = v.strip()

    if key not in config:
        raise RuntimeError(f"{key} が設定されていません")

    return config[key]