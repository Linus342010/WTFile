from pathlib import Path

def scan_files_and_folders(path):
    """
    Scans all files and folders in the given path (first level only).
    Returns a list of tuples: (name, size in bytes, type)
    Type is 'file' or 'folder'.
    """
    path = Path(path)
    results = []

    for item in path.iterdir():
        if item.is_file():
            size = item.stat().st_size
            results.append((item.name, size, 'file'))
        elif item.is_dir():
            folder_size = sum(f.stat().st_size for f in item.iterdir() if f.is_file())
            results.append((item.name, folder_size, 'folder'))

    return results
