from src.constants.constant import INPUT_ZERO, INPUT_ONE, INPUT_COMMANDS
from src.services.user import User
from src.constants.error_codes import ErrorCodes


# Class to process the input commands coming in
class ProcessInputCommands:
    def __init__(self):
        self._user = User()  # Keeping User instance private

    # Public method to process an input file
    def parse_input_file(self, file_path: str):
        with open(file_path, "r") as file:
            results = [self._parse_each_row(row.strip()) for row in file]
        return results

    # Private method to process each row
    def _parse_each_row(self, row: str):
        formatted_row = self._format_params(row.split(" "))
        command, params = formatted_row[INPUT_ZERO], formatted_row[INPUT_ONE:]
        return self._execute_command(command, params)

    # Private method to format parameters
    @staticmethod
    def _format_params(row: list):
        formatted_params = []
        for param in row:
            param = param.strip()
            try:
                formatted_params.append(int(param))
            except ValueError:
                formatted_params.append(param)
        return formatted_params

    # Private method to execute commands
    def _execute_command(self, command: str, params: list):
        if command not in INPUT_COMMANDS:
            raise ValueError(ErrorCodes.INVALID_INPUT)
        command_method = INPUT_COMMANDS[command]
        if not hasattr(self._user, command_method):
            raise AttributeError(f"{ErrorCodes.USER_ERROR_MSG} {command_method}")

        user_method = getattr(self._user, command_method)
        if callable(user_method):
            return user_method(*params) if params else user_method()
        else:
            raise TypeError(f"{command_method} {ErrorCodes.INVALID_INPUT}")
