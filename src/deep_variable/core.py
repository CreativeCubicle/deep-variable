from typing import Any, Union, Optional

class DeepVariable:
    @staticmethod
    def get(
        data: Union[dict, list], 
        path: str, 
        default: Any = None, 
        sep: str = "."
    ) -> Any:
        """
        Safely retrieves a value from a deeply nested structure using a string path.

        This method traverses dictionaries and lists iteratively. If a part of the 
        path is missing, or if a type mismatch occurs (e.g., trying to access a 
        list index on a dictionary), it returns the provided default value 
        instead of raising an exception.

        Args:
            data (Union[dict, list]): The nested object (dictionary or list) to search.
            path (str): A string representing the path to the desired value, 
                with components separated by `sep`. Integers in the path are 
                automatically treated as list indices.
            default (Any, optional): The value to return if the path does not exist 
                or an error occurs. Defaults to None.
            sep (str, optional): The delimiter used to split the path string. 
                Defaults to ".".

        Returns:
            Any: The value found at the specified path, or the `default` value.

        Examples:
            >>> data = {"users": [{"id": 1, "meta": {"login": "admin"}}]}
            >>> DeepVariable.get(data, "users.0.meta.login")
            'admin'
            >>> DeepVariable.get(data, "users.1.id", default="Not Found")
            'Not Found'
            >>> DeepVariable.get(data, "users/0/id", sep="/")
            1
        """
        if not path:
            return data

        keys = path.split(sep)
        current = data

        for key in keys:
            try:
                # Handle List Navigation
                if isinstance(current, list):
                    # We convert the key to int. If it fails, ValueError 
                    # is caught by the except block.
                    idx = int(key)
                    current = current[idx]
                # Handle Dict Navigation
                elif isinstance(current, dict):
                    current = current[key]
                else:
                    return default
            except (KeyError, IndexError, ValueError, TypeError):
                return default

        return current
    
    @staticmethod
    def has(data: Union[dict, list], path: str, sep: str = ".") -> bool:
        """
        Checks if a specific path exists within the nested structure.

        Unlike .get(), this returns True even if the value at the path is None, 
        False, or an empty string.

        Args:
            data (Union[dict, list]): The nested object to check.
            path (str): The path to verify.
            sep (str, optional): The path delimiter. Defaults to ".".

        Returns:
            bool: True if the path exists, False otherwise.
        """
        # Sentinel value to distinguish "not found" from "found None"
        sentinel = object()
        result = DeepVariable.get(data, path, default=sentinel, sep=sep)
        return result is not sentinel
    
    @staticmethod
    def set(data: dict, path: str, value: Any, sep: str = ".") -> bool:
        """
        Sets a value at a deeply nested path, creating intermediate dicts if missing.

        Note: Currently, this method primarily supports dictionary creation 
        for missing keys. It will not auto-create lists.

        Args:
            data (dict): The dictionary to modify (mutates in-place).
            path (str): The path where the value should be set.
            value (Any): The value to assign.
            sep (str, optional): The path delimiter. Defaults to ".".

        Returns:
            bool: True if the value was set successfully.
        """
        if not path:
            return False

        keys = path.split(sep)
        current = data

        # Navigate to the second-to-last element
        for i in range(len(keys) - 1):
            key = keys[i]
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        # Set the final value
        current[keys[-1]] = value
        return True