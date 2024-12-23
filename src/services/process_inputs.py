from src.constants.constant import INPUT_ZERO, INPUT_ONE, INPUT_COMMANDS
from src.services.user import User


# class to process the input commands comming
class ProcessInputCommands:
    def __init__(self):
        self.user = User()

    def parse_input_file(self, file_path):
        with open(file_path, "r") as file_obj:
            for row in file_obj:
                error_message = self.parse_each_row(row)
                if error_message:
                    break  # Stop further command processing

    def parse_each_row(self, row):
        row = row.split(" ")
        row = self.format_params(row)
        command, params = row[INPUT_ZERO], row[INPUT_ONE:]
        result = None
        if not params:
            result = getattr(self.user, INPUT_COMMANDS[command])()
        else:
            result = getattr(self.user, INPUT_COMMANDS[command])(*params)

        return result

    @staticmethod
    def format_params(row):
        ans = []
        for param in row:
            param = param.strip()
            try:
                param = int(param)
                ans.append(param)
            except:
                ans.append(param)
        return ans
