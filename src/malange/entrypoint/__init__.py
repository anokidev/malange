"""

    malange.entrypoint

    Contains the base class of Malange.

    Copyright (c) 2024 Anoki Youssou,
    all right reserved. Licensed in
    MIT License.

"""

from io import TextIOWrapper

class Malange:
    """
        This is the base class. The user will insert
        the contents of the file to the __init__()
    """

    def load_file(self, file_content: TextIOWrapper) -> None:
        """Load the data from a file."""

        self.data = file_content
