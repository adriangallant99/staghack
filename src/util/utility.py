import json

# Method 1 - Basic file reading
def read_json(file_path):
    """
    Read a JSON file and return

    Args:
        file_path (str): The path to the JSON file

    Returns:
        dict: A dictionary containing the JSON data
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error reading JSON: {str(e)}")
        return None
