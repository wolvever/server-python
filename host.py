import sys
import os

from server_python.app import App


class Host:
    def config(self, config):
        """Configures the host with the given settings."""
        pass

    def add_app(self, app: App):
        """Registers an application with the host."""
        pass

    def get_app(self, app_name: str) -> App:
        """Returns the named application registered with the host.
        
        Args:
            app_name (str): The type name of App, like 'EndpointApp'.
        """
        pass

    def get_runtime(self):
        pass

    def run(self):
        """Runs the host and blocks until it is stopped."""
        pass


def add_to_sys_path(directory_name, ):
    """
    Add the specified directory and its parent directories to sys.path.

    Args:
        directory_name (str): The name of the directory to add to sys.path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_cwd = os.path.dirname(os.getcwd())

    while not os.path.basename(current_dir) == directory_name:
        parent_dir = os.path.dirname(current_dir)
        print("current_dir", current_dir, "\tparent_dir", parent_dir)
        if parent_dir == current_dir:
            raise RuntimeError(f"Directory '{directory_name}' not found in path, current_dir reached.")
        if parent_dir == parent_cwd:
            raise RuntimeError(f"Directory '{directory_name}' not found in path, cwd reached.")

        current_dir = parent_dir
    
    # Add the directory to sys.path
    print(f"Adding directory '{current_dir}' to sys.path.")
    sys.path.append(current_dir)
