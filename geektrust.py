from sys import argv

# from src.services.command_line import CommandProcessor
from src.services.process_inputs import ProcessCommands


def main():
    """
    Sample code to read inputs from the file"""

    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, "r")
    Lines = f.readlines()
    c = ProcessCommands()
    c.process_input_commands(Lines)
    # c = CommandProcessor()
    # c.process_commands(Lines)


if __name__ == "__main__":
    main()
