import os
import platform
import subprocess
from os import path


def _explorer_path() -> str | None:
    return path.join(os.getenv("WINDIR"), "explorer.exe") if os.getenv("WINDIR") else None


def can_find_explorer() -> bool:
    return bool(platform.system() == "Windows" and _explorer_path() and path.exists(_explorer_path()))


def explore_to_file(file_path: str) -> None:
    if not can_find_explorer():
        raise Exception("Cannot find Windows Explorer")
    # Explorer wants the quotes around the path alone, not around the whole "/select,path" argument.
    # Passing a sequence to Popen would quote the entire argument when the path contains spaces,
    # which Explorer fails to parse, silently opening the default folder instead. Hence the
    # hand-built command line. normpath is needed because Blender may hand back forward slashes.
    native_path = path.normpath(file_path)
    subprocess.Popen(f'"{_explorer_path()}" /select,"{native_path}"')
