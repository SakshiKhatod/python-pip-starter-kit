from sys import argv
from src.services.command_line import process_commands


def main():
    """
    Sample code to read inputs from the file"""

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, "r")
    Lines = f.readlines()
    process_commands(Lines)


if __name__ == "__main__":
    main()
