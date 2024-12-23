import sys
from src.services.process_inputs import ProcessInputCommands


def main(file_path):

    c = ProcessInputCommands()
    c.parse_input_file(file_path)


if __name__ == "__main__":

    file_path = sys.argv[1]
    main(file_path)
