import sys
from terminaltables import AsciiTable

from src.scan_file import *
from src.utils import *

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
                scan = scann_only_folders(path)
            else:
                path = Path(input_path)
                scan = scann_only_folders(path)
            print_results(scan)
        else:
            pass

if __name__ == "__main__":
    main()
    input("\nPress ENTER to exit...")