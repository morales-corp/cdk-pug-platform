import os
from dotenv import load_dotenv

from enum import Enum


class PathTypes(Enum):
    FILE = "file"
    FOLDER = "folder"
    DOT_ENV = ".env"
    UNKNOWN = "unknown"


class PathDispatcher:
    def __init__(self, absolute_path: str):
        self.absolute_patch = absolute_path

    def dispatch(self):
        is_dotenv = self.absolute_patch.endswith(".env")
        is_file = os.path.isfile(self.absolute_patch)
        is_folder = os.path.isdir(self.absolute_patch)

        if is_dotenv:
            PathTypes.DOT_ENV._value_ = self.absolute_patch.split("/")[-1]
            return PathTypes.DOT_ENV
        elif is_file:
            PathTypes.FILE._value_ = self.absolute_patch.split("/")[-1]
            return PathTypes.FILE
        elif is_folder:
            PathTypes.FOLDER._value_ = self.absolute_patch.split("/")[-1]
            return PathTypes.FOLDER
        else:
            PathTypes.UNKNOWN._value_ = self.absolute_patch.split("/")[-1]
            return PathTypes.UNKNOWN


class EnvironmentValidator:
    @staticmethod
    def validate(absolute_patch: str):
        """
        Validates and loads a file based on its path type.
        This function determines the type of file at the given path, attempts to load it,
        and provides visual feedback about the loading process through console output.
        For .env files, it specifically attempts to load environment variables.
        Args:
            absolute_patch (str): The absolute path to the file that needs to be validated.
        Returns:
            None
        Raises:
            Exception: If the file does not exist or if a .env file fails to load.
        Example:
            >>> validate("/path/to/your/file.env")
            ✨ Loading .env Path: /path/to/your/file.env
            🟢 Loaded .env: /path/to/your/file.env
        """

        file_type = PathDispatcher(absolute_patch).dispatch()

        print(
            f"\033[1;33m✨ Loading {file_type.value} Path: \033[1;33m{absolute_patch}\033[0m"
        )
        if not os.path.exists(absolute_patch):
            print(f"\033[1;31m❌ {file_type.value} not found: {absolute_patch}\033[0m")
            raise Exception(f"{file_type.value} not found: {absolute_patch}")

        if file_type == PathTypes.DOT_ENV:
            dotenv_success = load_dotenv(
                absolute_patch,
                override=True,
            )
            if not dotenv_success:
                print(
                    f"\033[1;31m❌ Failed to load {file_type.value}: {absolute_patch}\033[0m"
                )
                print(
                    f"\033[1;31m❌ Check if the {file_type.value} is empty or malformed\033[0m"
                )
                raise Exception(f"Failed to load {file_type.value}: {absolute_patch}")
        print(
            f"\033[1;32m🟢 Loaded {file_type.value}: \033[1;33m{absolute_patch}\033[0m"
        )
