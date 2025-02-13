import sys
import gzip
import zipfile
import os
import re

# Adjust these paths as needed
ZIP_ARCHIVE_PATH = "C:/Users/YASHK/OneDrive/Desktop/Farmart/logs_2024.log.zip"
OUTPUT_DIRECTORY = "output"

def ensure_output_folder_exists(folder_path):
    """
    Creates the specified folder if it doesn't already exist.
    """
    os.makedirs(folder_path, exist_ok=True)

def is_valid_zip_file(path):
    """
    Checks if a file exists and is recognized by Python's zipfile module.
    """
    if not os.path.exists(path):
        print("Error: ZIP file not found.")
        return False
    if not zipfile.is_zipfile(path):
        print("Error: The specified file is not a valid ZIP archive.")
        return False
    return True

def build_output_file_path(folder_path, date_string):
    """
    Constructs the output file path using the target date.
    """
    return os.path.join(folder_path, f"output_{date_string}.txt")

def build_start_pattern(date_string):
    """
    Creates a compiled regex pattern to match lines that begin with the given date string.
    """
    return re.compile(rf'^{re.escape(date_string)}')

def is_log_or_gz(filename):
    """
    Determines whether a file is a .log or .gz file.
    """
    return filename.endswith('.log') or filename.endswith('.gz')

def open_compressed_if_needed(zip_ref, filename):
    """
    Opens a file from inside a ZIP. If it's .gz, use gzip; otherwise, return the raw file handle.
    """
    raw = zip_ref.open(filename)  # ZipExtFile object
    if filename.endswith('.gz'):
        return gzip.open(raw)
    return raw

def process_logs_in_zip(zip_path, target_pattern, output_file_path):
    """
    Iterates through files in the ZIP archive, filters lines by target_pattern,
    and writes matching lines to the output file.
    """
    with zipfile.ZipFile(zip_path, 'r') as zf, open(output_file_path, 'w', encoding='utf-8') as out:
        for member in zf.namelist():
            if is_log_or_gz(member):
                with open_compressed_if_needed(zf, member) as log_data:
                    for raw_line in log_data:
                        decoded_line = raw_line.decode('utf-8', errors='ignore')
                        if target_pattern.match(decoded_line):
                            out.write(decoded_line)

def extract_logs(target_date):
    """
    Main extraction routine. Validates the ZIP file, prepares an output file,
    and filters lines by the given date.
    """
    if not is_valid_zip_file(ZIP_ARCHIVE_PATH):
        return  # Error already printed inside is_valid_zip_file
    
    ensure_output_folder_exists(OUTPUT_DIRECTORY)
    output_path = build_output_file_path(OUTPUT_DIRECTORY, target_date)
    
    pattern = build_start_pattern(target_date)
    
    try:
        process_logs_in_zip(ZIP_ARCHIVE_PATH, pattern, output_path)
        print(f"Filtered log entries saved to {output_path}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py <target_date>")
        return
    date_arg = sys.argv[1]
    extract_logs(date_arg)

if __name__ == "__main__":
    main()
