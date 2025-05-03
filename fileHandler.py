import os

def clean_dat_file(dat_file_path:str, clean_dat_file_path:str) -> None:
    """
    Replaces soi.dat file content with the content of clean soi.dat file. 
    Prerequisite: You must prepare a clean soi.dat file.
    Args:
        dat_file_path (str): Path to the original .dat file. Could be a relative or absolute path.
        clean_dat_file_path (str): Path to the clean .dat file. Could be a relative or absolute path.
    """
    try:
        with open(dat_file_path, 'w') as dat_file:
            with open(clean_dat_file_path, 'r') as clean_dat_file:
                dat_file.write(clean_dat_file.read())
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error cleaning .dat file: {e}")

def copy_dat_file(dat_file_path:str, copy_dat_file_path:str) -> None:
    """
    Copies the content of the original .dat file to a new .dat file.
    Args:
        dat_file_path (str): Path to the original .dat file. Could be a relative or absolute path.
        copy_dat_file_path (str): Path to the copied .dat file. Could be a relative or absolute path.
    """
    try:
        # Ensure the directory for the copy file exists
        os.makedirs(os.path.dirname(copy_dat_file_path), exist_ok=True)
        
        with open(dat_file_path, 'r') as dat_file:
            with open(copy_dat_file_path, 'w') as copy_dat_file:
                copy_dat_file.write(dat_file.read())
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Error copying .dat file: {e}")

def compare_dat_to_expected(dat_file_path:str, expected_dat_file_path:str) -> bool:
    """
    Compares the content of the original .dat file with the expected .dat file.
    Args:
        dat_file_path (str): Path to the original .dat file. Could be a relative or absolute path.
        expected_dat_file_path (str): Path to the expected .dat file. Could be a relative or absolute path.
    Returns:
        bool: True if the files are identical, False otherwise.
    """
    try:
        with open(dat_file_path, 'r') as dat_file:
            with open(expected_dat_file_path, 'r') as expected_dat_file:
                return dat_file.read() == expected_dat_file.read()
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False
    except Exception as e:
        print(f"Error comparing .dat files: {e}")
        return False