import sys
import os

def append_null_byte(file_path):
    """
    Appends a single null byte (0x00) to the end of the specified file.
    
    Args:
        file_path (str): The path to the file to be modified.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Check if the path is a valid file (not a directory)
        if not os.path.isfile(file_path):
            print(f"Error: '{file_path}' is not a valid file.")
            return False
        
        # Append the null byte in binary mode
        with open(file_path, 'ab') as file:
            file.write(b'\x00')
        print(f"Successfully appended null byte to: {file_path}")
        return True
    except PermissionError:
        print(f"Error: Permission denied when accessing '{file_path}'.")
    except IOError as e:
        print(f"Error: Could not modify file '{file_path}'. {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return False

if __name__ == "__main__":
    # Check if file paths are provided via drag-and-drop
    if len(sys.argv) < 2:
        input("Drag and drop one or more files onto this script, then press Enter to exit...")
    else:
        # Process all dropped files
        for i, file_path in enumerate(sys.argv[1:], start=1):
            print(f"Processing file {i}: {file_path}")
            success = append_null_byte(file_path)
            if not success:
                print(f"Failed to process: {file_path}")
        print("All files processed.")