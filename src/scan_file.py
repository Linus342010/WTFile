from pathlib import Path
import os
from terminaltables import AsciiTable


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


def scan_files_in_subfolders(path):
    """
    Scans all files in all subfolders of the given path.
    Returns a list of tuples: (name, size in bytes, type)
    Type is 'file'.
    """
    path = Path(path)
    results = []

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = Path(root) / file
            size = file_path.stat().st_size
            results.append((str(file_path.relative_to(path)), size, 'file'))

    return results


def scann_only_folders(path):
    """
    Scans only folders in the given path (first level only).
    Returns a list of tuples: (name, size in bytes, type)
    Type is 'folder'.
    """
    path = Path(path)
    results = []

    for item in path.iterdir():
        if item.is_dir():
            folder_size = sum(f.stat().st_size for f in item.iterdir() if f.is_file())
            results.append((item.name, folder_size, 'folder'))

    return results


def format_size(size):
    """Formatiert die Größe in Byte, KB, MB oder GB."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"  # falls es extrem große Dateien gibt


def print_results(results):
    table_data = [['Name', 'Größe', 'Typ']]

    for name, size, typ in results:
        table_data.append([name, format_size(size), typ])

    table = AsciiTable(table_data)
    print(table.table)

