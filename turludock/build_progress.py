import re
from typing import Tuple, Optional
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TextColumn


class BuildProgress:
    """A class used to track progress of a docker build process."""

    def __init__(self) -> None:
        """Initializes a BuildProgress object.

        The object is used to track progress of a docker build process.

        The Progress object is configured to show the description of the task, a progress bar,
        the percentage completed and the time elapsed.

        The object has three attributes:
            - total_tasks: The total number of tasks
            - is_initialized: Whether the progress bar is initialized or not
            - progress: The Progress object
            - task: The Task object representing the current task. This is set when the progress bar
                      is initialized.
        """
        self.total_tasks = 0
        self.is_initialized = False
        self.progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeElapsedColumn(),
        )
        self.task = None

    def find_and_parse_extra_step(self, status_msg: str) -> Tuple[bool, Optional[int], Optional[int]]:
        """Parses the docker build output and looks for the "Step m/n" pattern.

        This is then used to determine the progress of the docker build command.

        The function uses regex to find the pattern in the input string.
        The function returns a tuple with a boolean indicating whether the pattern was found
        or not and two optional integers representing the "Step m/n".

        Args:
            status_msg (str): The string to search for the pattern in.

        Returns:
            Tuple[bool, Optional[int], Optional[int]]: A tuple with a boolean and two optional integers.
        """
        # Define the regex pattern to match "Step NUMBER_ONE/NUMBER_TWO :"
        pattern = r"Step (\d+)/(\d+) :"

        # Use re.search to find the pattern in the input string
        match = re.search(pattern, status_msg)

        if match:
            # Extract the two numbers and convert them to integers
            number_one = int(match.group(1))
            number_two = int(match.group(2))
            return True, number_one, number_two
        else:
            return False, None, None

    def _start(self, total_tasks: int) -> None:
        """Initializes the progress bar based on the total steps the build command has.

        Args:
            total_tasks (int): The total number of steps the build command has.
        """
        self.total_tasks = total_tasks
        self.task = self.progress.add_task("[green]|Building...", total=self.total_tasks)
        self.progress.start()
        self.is_initialized = True

    def finish(self) -> None:
        """Stops the progress bar."""
        self.progress.stop()

    def advance(self, build_status_msg: str) -> None:
        """Advances the progress bar based on the docker build status message.

        To determine the progress, the function uses regex to find the "Step m/n" pattern.

        Args:
            build_status_msg (str): The docker build status message.
        """
        # Parse docker build status message to check progress
        found, _, total_tasks = self.find_and_parse_extra_step(build_status_msg)

        # If status message contains progress update the bar
        if found:
            if not self.is_initialized:
                self._start(total_tasks)
            # Update bar
            # print(f"Step: {step}/{total_tasks}")
            self.progress.advance(self.task, advance=1)
