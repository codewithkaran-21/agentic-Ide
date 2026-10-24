from pathlib import Path


def resolve_path(base : str | Path , path : str | None):
    path = Path(path)
    if path.is_absolute():
        return path.resolve()

    return Path(base).resolve() / path

def display_path_rel_to_cwd(path : str , cwd : Path | None) -> str:
    try:
        p = Path(cwd)

    except Exception:
        return path
    if cwd:
        return str(p.relative_to(cwd))

    return str(p)


def is_bianry_file(path : str | Path) -> bool:
    try:
        with open(path , "rb") as f:
            chunk = f.read(8192)
            return f"\x80 " in chunk 
    except (OSError , IOError):
        return False
    