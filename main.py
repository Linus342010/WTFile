import sys

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


def scan_only_folders(path):
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
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def print_results(results):
    table_data = [['name', 'size', 'type']]

    for name, size, typ in results:
        table_data.append([name, format_size(size), typ])

    table = AsciiTable(table_data)
    print(table.table)


# menu input
try:
    # Windows
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
except ImportError:
    # Linux / macOS
    import tty
    import termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

#Menu
def terminal_menu():
    red = "\033[31m"
    white = "\033[37m"
    reset = "\033[0m"

    lines = [
        red + "                         ██╗    ██╗████████╗" + white + " ███████╗██╗██╗     ███████╗",
        red + "                         ██║    ██║╚══██╔══╝" + white + " ██╔════╝██║██║     ██╔════╝",
        red + "                         ██║ █╗ ██║   ██║   " + white + " █████╗  ██║██║     █████╗  ",
        red + "                         ██║███╗██║   ██║   " + white + " ██╔══╝  ██║██║     ██╔══╝  ",
        red + "                         ╚███╔███╔╝   ██║   " + white + " ██║     ██║███████╗███████╗",
        red + "                          ╚══╝╚══╝    ╚═╝   " + white + " ╚═╝     ╚═╝╚══════╝╚══════╝" + reset
    ]

    print("\n" * 2)
    for line in lines:
        print(line)
    print("\n")

    print("""
[1]...Scan all files and folders
[2]...Scan all files in all subfolders
[3]...Scan only folders
""")

# Main
def main():
    while True:
        terminal_menu()

        while True:
            menu_choice = getch()
            if menu_choice == "1": #files and folders
                input_path = input("\nEnter the path to scan: (Press ENTER to use current directory)")
                if input_path == "":
                    path = Path.cwd()
                    scan = scan_files_and_folders(path)
                else:
                    path = Path(input_path)
                    scan = scan_files_and_folders(path)
                print_results(scan)
            elif menu_choice == "2":
                input_path = input("\nEnter the path to scan: (Press ENTER to use current directory)")
                if input_path == "":
                    path = Path.cwd()
                    scan = scan_files_in_subfolders(path)
                else:
                    path = Path(input_path)
                    scan = scan_files_in_subfolders(path)
                print_results(scan)
            elif menu_choice == "3":
                input_path = input("\nEnter the path to scan: (Press ENTER to use current directory)")
                if input_path == "":
                    path = Path.cwd()
                    scan = scan_only_folders(path)
                else:
                    path = Path(input_path)
                    scan = scan_only_folders(path)
                print_results(scan)
            
            else:
                break
        break

if __name__ == "__main__":
    main()