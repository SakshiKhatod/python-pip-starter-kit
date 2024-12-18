from sys import argv

# from src.services.commands import process_commands
from src.services.command_line import CommandProcessor


def main():
    """
    Sample code to read inputs from the file"""

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, "r")
    Lines = f.readlines()
    c = CommandProcessor()
    c.process_commands(Lines)
    # process_commands(Lines)


if __name__ == "__main__":
    main()
