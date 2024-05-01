import toml
from pathlib import Path


def get_version() -> str:
    abs_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
    try:
        with open(abs_path) as file:
            data = toml.load(file)
        return data["tool"]["poetry"]["version"]
    except Exception as e:
        return "0.0.0"
    finally:
        file.close()


if __name__ == "__main__":
    print(get_version())
